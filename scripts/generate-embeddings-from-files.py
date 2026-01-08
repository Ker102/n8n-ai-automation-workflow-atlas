"""
Generate embeddings from current workflow files using Together AI.
Reads directly from workflows/ directory for accurate ID matching.

Usage: 
  export TOGETHER_API_KEY=your_key
  python scripts/generate-embeddings-from-files.py
"""

import json
import time
import os
from pathlib import Path

try:
    from together import Together
except ImportError:
    print("Installing together package...")
    os.system("pip install together -q")
    from together import Together

# Configuration
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
OUTPUT_FILE = Path(__file__).parent.parent / "embeddings_current.jsonl"
MODEL_NAME = "togethercomputer/m2-bert-80M-32k-retrieval"
BATCH_SIZE = 50
DELAY_BETWEEN_BATCHES = 0.5

def walk_dir(dir_path):
    """Recursively get all JSON files."""
    files = []
    for item in dir_path.iterdir():
        if item.is_dir():
            files.extend(walk_dir(item))
        elif item.suffix == ".json":
            files.append(item)
    return files

def create_search_text(workflow, file_path):
    """Create searchable text from workflow content."""
    parts = []
    
    # Workflow name
    if workflow.get("name"):
        parts.append(f"Name: {workflow['name']}")
    
    # File name (for matching)
    parts.append(f"File: {file_path.stem}")
    
    # Category from path
    rel_path = file_path.relative_to(WORKFLOWS_DIR)
    category = rel_path.parts[0] if len(rel_path.parts) > 1 else "unknown"
    parts.append(f"Category: {category}")
    
    # Get nodes info
    nodes = workflow.get("nodes", [])
    node_types = set()
    for node in nodes[:15]:  # Limit nodes
        node_type = node.get("type", "")
        if "n8n-nodes-base." in node_type:
            node_types.add(node_type.replace("n8n-nodes-base.", ""))
    if node_types:
        parts.append(f"Integrations: {', '.join(sorted(node_types))}")
    
    # Complexity
    complexity = workflow.get("meta", {}).get("complexity", "unknown")
    parts.append(f"Complexity: {complexity}")
    
    # Description if available
    if workflow.get("description"):
        parts.append(f"Description: {workflow['description'][:200]}")
    
    return " | ".join(parts)

def main():
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        print("Error: TOGETHER_API_KEY not set")
        return
    
    client = Together(api_key=api_key)
    
    # Load existing to resume
    existing_ids = set()
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        existing_ids.add(json.loads(line).get("file_id"))
                    except:
                        pass
        print(f"Found {len(existing_ids)} existing embeddings, resuming...")
    
    # Get all workflow files
    print("Scanning workflow files...")
    all_files = walk_dir(WORKFLOWS_DIR)
    print(f"Found {len(all_files)} workflow files")
    
    # Filter out already processed
    files_to_process = [f for f in all_files if f.stem not in existing_ids]
    print(f"Processing {len(files_to_process)} new files...\n")
    
    if not files_to_process:
        print("All files already processed!")
        return
    
    processed = len(existing_ids)
    total = len(all_files)
    
    with open(OUTPUT_FILE, 'a') as out_f:
        for i in range(0, len(files_to_process), BATCH_SIZE):
            batch_files = files_to_process[i:i + BATCH_SIZE]
            
            # Load workflows and create texts
            batch_data = []
            texts = []
            for f in batch_files:
                try:
                    workflow = json.loads(f.read_text())
                    text = create_search_text(workflow, f)
                    batch_data.append({
                        "file_path": str(f),
                        "file_id": f.stem,
                        "workflow_name": workflow.get("name", f.stem),
                        "category": f.relative_to(WORKFLOWS_DIR).parts[0]
                    })
                    texts.append(text)
                except Exception as e:
                    print(f"Error reading {f}: {e}")
                    continue
            
            if not texts:
                continue
            
            # Generate embeddings
            try:
                response = client.embeddings.create(
                    model=MODEL_NAME,
                    input=texts
                )
                
                for j, embedding_data in enumerate(response.data):
                    result = {
                        **batch_data[j],
                        "embedding": embedding_data.embedding
                    }
                    out_f.write(json.dumps(result) + "\n")
                
                processed += len(batch_data)
                print(f"Progress: {processed}/{total} ({100*processed/total:.1f}%)")
                
                time.sleep(DELAY_BETWEEN_BATCHES)
                
            except Exception as e:
                print(f"Error: {e}")
                if "rate" in str(e).lower():
                    print("Rate limited, waiting 30s...")
                    time.sleep(30)
                continue
    
    print(f"\nDone! Embeddings saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
