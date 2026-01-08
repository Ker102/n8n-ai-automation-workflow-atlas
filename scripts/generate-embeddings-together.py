"""
Generate embeddings for workflows using Together AI API.
Uses BGE-Large-EN model (768 dimensions, high quality).

Usage: 
  export TOGETHER_API_KEY=your_key
  python scripts/generate-embeddings-together.py
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
INPUT_FILE = Path(__file__).parent.parent / "n8n_workflows.jsonl"
OUTPUT_FILE = Path(__file__).parent.parent / "embeddings_together.jsonl"
MODEL_NAME = "togethercomputer/m2-bert-80M-32k-retrieval"  # 32k context, great for workflows
BATCH_SIZE = 50  # Together AI handles larger batches well
DELAY_BETWEEN_BATCHES = 0.5  # seconds

def create_search_text(record: dict) -> str:
    """Create a searchable text from workflow metadata."""
    parts = []
    
    if record.get("name"):
        parts.append(f"Name: {record['name']}")
    if record.get("category"):
        parts.append(f"Category: {record['category']}")
    if record.get("description"):
        parts.append(f"Description: {record['description']}")
    if record.get("instruction"):
        parts.append(f"Instruction: {record['instruction']}")
    if record.get("archetype"):
        parts.append(f"Archetype: {record['archetype']}")
    if record.get("tools"):
        tools = record["tools"][:10] if isinstance(record["tools"], list) else [record["tools"]]
        parts.append(f"Tools: {', '.join(str(t) for t in tools)}")
    
    return " | ".join(parts) if parts else record.get("name", "Unknown workflow")

def main():
    # Check for API key
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        print("Error: TOGETHER_API_KEY environment variable not set")
        print("Get your key from: https://api.together.xyz/")
        return
    
    client = Together(api_key=api_key)
    
    # Load existing embeddings to resume
    existing_ids = set()
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        existing_ids.add(json.loads(line).get("id"))
                    except:
                        pass
        print(f"Found {len(existing_ids)} existing embeddings, resuming...")
    
    # Load records
    records = []
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                record_id = record.get("id") or record.get("name")
                if record_id not in existing_ids:
                    records.append(record)
    
    print(f"Processing {len(records)} new records...")
    
    # Process in batches
    processed = len(existing_ids)
    total = processed + len(records)
    
    with open(OUTPUT_FILE, 'a') as out_f:
        for i in range(0, len(records), BATCH_SIZE):
            batch = records[i:i + BATCH_SIZE]
            texts = [create_search_text(r) for r in batch]
            
            try:
                response = client.embeddings.create(
                    model=MODEL_NAME,
                    input=texts
                )
                
                for j, embedding_data in enumerate(response.data):
                    record = batch[j]
                    result = {
                        "id": record.get("id") or record.get("name"),
                        "name": record.get("name"),
                        "category": record.get("category"),
                        "embedding": embedding_data.embedding
                    }
                    out_f.write(json.dumps(result) + "\n")
                
                processed += len(batch)
                print(f"Progress: {processed}/{total} ({100*processed/total:.1f}%)")
                
                time.sleep(DELAY_BETWEEN_BATCHES)
                
            except Exception as e:
                print(f"Error at batch {i}: {e}")
                if "rate" in str(e).lower():
                    print("Rate limited, waiting 30s...")
                    time.sleep(30)
                continue
    
    print(f"\nDone! Embeddings saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
