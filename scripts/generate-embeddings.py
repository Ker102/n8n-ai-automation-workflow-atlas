"""
Generate embeddings for n8n workflows using Vertex AI Gemini Embedding 001.

Prerequisites:
1. Install: pip install google-genai
2. Set environment:
   export GOOGLE_CLOUD_PROJECT=nimble-depot-450414-j4
   export GOOGLE_CLOUD_LOCATION=global
   export GOOGLE_GENAI_USE_VERTEXAI=True
3. Authenticate: gcloud auth application-default login

Usage:
    python scripts/generate-embeddings.py
"""

import json
import os
import time
from pathlib import Path
from google import genai
from google.genai.types import EmbedContentConfig

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "nimble-depot-450414-j4")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
INPUT_FILE = Path(__file__).parent.parent / "n8n_workflows.jsonl"
OUTPUT_FILE = Path(__file__).parent.parent / "embeddings.jsonl"
BATCH_SIZE = 20  # Smaller batch size to avoid quota issues
MODEL_NAME = "gemini-embedding-001"
OUTPUT_DIMENSIONS = 768  # Use smaller dimensions for efficiency (max 3072)

# Rate limiting
DELAY_BETWEEN_BATCHES = 2.0  # seconds
RETRY_DELAY = 30.0  # seconds on quota error
MAX_RETRIES = 3

def create_search_text(record: dict) -> str:
    """Create searchable text from workflow record."""
    parts = []
    
    # Name
    if record.get("name"):
        parts.append(f"Name: {record['name']}")
    
    # Description/instruction from meta
    if record.get("meta"):
        if record["meta"].get("description"):
            parts.append(f"Description: {record['meta']['description']}")
        if record["meta"].get("instruction"):
            parts.append(f"Instruction: {record['meta']['instruction']}")
        if record["meta"].get("archetype"):
            parts.append(f"Archetype: {record['meta']['archetype']}")
    
    # Category
    if record.get("category"):
        parts.append(f"Category: {record['category']}")
    
    # Integrations (tools used)
    if record.get("integrations"):
        parts.append(f"Tools: {', '.join(record['integrations'])}")
    
    return " | ".join(parts) if parts else record.get("name", "Unknown workflow")

def main():
    print(f"Initializing Google GenAI with project: {PROJECT_ID}")
    
    # Set environment for Vertex AI
    os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
    os.environ["GOOGLE_CLOUD_LOCATION"] = LOCATION
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    
    client = genai.Client()
    
    print(f"Reading workflows from: {INPUT_FILE}")
    
    # Read all records
    records = []
    with open(INPUT_FILE, 'r') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    
    print(f"Total workflows: {len(records)}")
    print(f"Batch size: {BATCH_SIZE}, Delay: {DELAY_BETWEEN_BATCHES}s")
    print(f"Estimated time: {len(records) / BATCH_SIZE * DELAY_BETWEEN_BATCHES / 60:.1f} minutes\n")
    
    # Check for existing progress
    existing_ids = set()
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        existing_ids.add(json.loads(line).get("id"))
                    except:
                        pass
        print(f"Resuming: {len(existing_ids)} embeddings already generated")
    
    # Filter out already processed
    records = [r for r in records if r.get("id") not in existing_ids]
    print(f"Remaining to process: {len(records)}\n")
    
    # Process in batches with rate limiting
    processed = len(existing_ids)
    with open(OUTPUT_FILE, 'a') as out_f:
        for i in range(0, len(records), BATCH_SIZE):
            batch = records[i:i + BATCH_SIZE]
            texts = [create_search_text(r) for r in batch]
            
            for retry in range(MAX_RETRIES):
                try:
                    response = client.models.embed_content(
                        model=MODEL_NAME,
                        contents=texts,
                        config=EmbedContentConfig(
                            task_type="RETRIEVAL_DOCUMENT",
                            output_dimensionality=OUTPUT_DIMENSIONS,
                        ),
                    )
                    
                    # Write results
                    for record, embedding in zip(batch, response.embeddings):
                        result = {
                            "id": record.get("id"),
                            "name": record.get("name"),
                            "category": record.get("category"),
                            "embedding": embedding.values
                        }
                        out_f.write(json.dumps(result) + "\n")
                    
                    processed += len(batch)
                    print(f"Processed {processed}/{len(existing_ids) + len(records)} workflows")
                    
                    # Rate limiting delay
                    time.sleep(DELAY_BETWEEN_BATCHES)
                    break
                    
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        if retry < MAX_RETRIES - 1:
                            print(f"Rate limited, waiting {RETRY_DELAY}s (retry {retry+1}/{MAX_RETRIES})")
                            time.sleep(RETRY_DELAY)
                        else:
                            print(f"Failed after {MAX_RETRIES} retries: {e}")
                    else:
                        print(f"Error: {e}")
                        break
    
    print(f"\nEmbeddings saved to: {OUTPUT_FILE}")
    print(f"Total processed: {processed}")

if __name__ == "__main__":
    main()
