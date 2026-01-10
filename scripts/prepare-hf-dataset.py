"""
Prepare training-ready dataset for HuggingFace upload.
Enhances metadata and creates proper instruction/output pairs.

Usage: python scripts/prepare-hf-dataset.py
"""

import json
from pathlib import Path
from datetime import datetime

# Configuration  
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
OUTPUT_DIR = Path(__file__).parent.parent / "hf_dataset"
FOLDERS = ["synthetic_v2", "synthetic", "external", "ai-automation-lab", "initial_megapack"]

def walk_dir(dir_path):
    files = []
    if not dir_path.exists():
        return files
    for item in dir_path.iterdir():
        if item.is_dir():
            files.extend(walk_dir(item))
        elif item.suffix == ".json":
            files.append(item)
    return files

def has_valid_skeleton(workflow):
    """Check for valid connections."""
    connections = workflow.get("connections", {})
    if not connections:
        return False
    connected = set()
    for source, data in connections.items():
        connected.add(source)
        for outputs in data.get("main", []):
            if isinstance(outputs, list):
                for c in outputs:
                    if isinstance(c, dict) and "node" in c:
                        connected.add(c["node"])
    nodes = workflow.get("nodes", [])
    return len(connected) >= len(nodes) * 0.5 if nodes else False

def extract_node_types(workflow):
    """Get list of node types used."""
    nodes = workflow.get("nodes", [])
    types = []
    for n in nodes:
        t = n.get("type", "").replace("n8n-nodes-base.", "")
        if t and t not in types:
            types.append(t)
    return types

def create_instruction(workflow, node_types):
    """Create natural language instruction."""
    name = workflow.get("name", "Workflow")
    meta = workflow.get("meta", {})
    label = meta.get("semanticLabel", "")
    
    # Build instruction
    parts = []
    parts.append(f"Create an n8n workflow to: {name}")
    if label:
        parts.append(f"Category: {label}")
    if node_types:
        parts.append(f"Using: {', '.join(node_types[:6])}")
    
    return " | ".join(parts)

def main():
    print("Preparing HuggingFace dataset...\n")
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    all_files = []
    for folder in FOLDERS:
        folder_path = WORKFLOWS_DIR / folder
        files = walk_dir(folder_path)
        all_files.extend(files)
        print(f"  {folder}: {len(files)} files")
    
    print(f"\nTotal: {len(all_files)} files\n")
    
    # Output files
    train_file = OUTPUT_DIR / "train.jsonl"
    metadata_file = OUTPUT_DIR / "metadata.json"
    
    stats = {"valid": 0, "invalid": 0, "total": 0}
    categories = {}
    
    with open(train_file, 'w') as f:
        for i, file_path in enumerate(all_files):
            if i % 10000 == 0:
                print(f"Progress: {i}/{len(all_files)}")
            
            try:
                workflow = json.loads(file_path.read_text())
                
                if not has_valid_skeleton(workflow):
                    stats["invalid"] += 1
                    continue
                
                node_types = extract_node_types(workflow)
                meta = workflow.get("meta", {})
                
                # Create training example
                example = {
                    "instruction": create_instruction(workflow, node_types),
                    "input": "",
                    "output": json.dumps(workflow),
                    "category": meta.get("semanticLabel", "general"),
                    "complexity": meta.get("complexity", "intermediate"),
                    "node_count": len(workflow.get("nodes", [])),
                    "source": file_path.parts[-2] if len(file_path.parts) > 1 else "unknown",
                    "is_generated": meta.get("generated", False)
                }
                
                f.write(json.dumps(example) + "\n")
                stats["valid"] += 1
                
                # Track categories
                cat = meta.get("semanticLabel", "other")
                categories[cat] = categories.get(cat, 0) + 1
                
            except Exception as e:
                stats["invalid"] += 1
    
    # Save metadata
    metadata = {
        "dataset_name": "n8n-workflows-atlas",
        "version": "2.0",
        "created_at": datetime.now().isoformat(),
        "total_examples": stats["valid"],
        "invalid_skipped": stats["invalid"],
        "categories": dict(sorted(categories.items(), key=lambda x: -x[1])),
        "description": "High-quality n8n workflow dataset for training workflow generators",
        "license": "Apache-2.0",
        "features": {
            "instruction": "Natural language description of what the workflow does",
            "input": "Optional additional context (empty for most)",
            "output": "Complete n8n workflow JSON",
            "category": "Semantic category (25 categories)",
            "complexity": "basic/intermediate/advanced",
            "node_count": "Number of nodes in workflow",
            "source": "Source folder",
            "is_generated": "Whether synthetically generated"
        }
    }
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n=== COMPLETE ===")
    print(f"Valid examples: {stats['valid']}")
    print(f"Invalid skipped: {stats['invalid']}")
    print(f"Categories: {len(categories)}")
    print(f"\nSaved to: {OUTPUT_DIR}")
    print(f"  - train.jsonl ({stats['valid']} examples)")
    print(f"  - metadata.json")

if __name__ == "__main__":
    main()
