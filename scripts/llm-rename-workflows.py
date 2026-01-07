"""
LLM-based workflow naming using Gemini API.
Generates descriptive names for workflows based on their content.

Usage:
  python scripts/llm-rename-workflows.py

Models used:
  - Primary: gemini-2.5-pro-preview-05-06 (10k requests/day)
  - Fallback: gemini-2.0-flash (no daily limit)
"""

import json
import os
import time
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai

# Configuration
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
FOLDERS_TO_PROCESS = ["synthetic", "external"]  # Only process these folders
OUTPUT_LOG = Path(__file__).parent.parent / "rename_log.jsonl"
BATCH_SIZE = 10  # Workflows per API call
DELAY_BETWEEN_CALLS = 0.5  # seconds
MAX_RETRIES = 3

# Models
PRIMARY_MODEL = "gemini-2.0-flash"  # Fast, high limit
FALLBACK_MODEL = "gemini-1.5-flash"  # Backup

# Prompt template
PROMPT_TEMPLATE = """You are naming n8n automation workflows. Generate a short, descriptive filename for each workflow.

Guidelines:
- Use lowercase with underscores (snake_case)
- Max 50 characters
- Focus on WHAT the workflow does, not the tools used
- Be specific and unique
- No file extension needed

For each workflow, respond with ONLY the new name, one per line.

Workflows:
{workflows}

New names (one per line):"""

def sanitize_filename(name: str) -> str:
    """Clean up generated name to be a valid filename."""
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9_]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')[:50]
    return name or "unnamed_workflow"

def extract_workflow_summary(workflow: dict) -> str:
    """Create a summary of what the workflow does."""
    parts = []
    
    # Get workflow name
    name = workflow.get("name", "")
    if name:
        parts.append(f"Name: {name}")
    
    # Get nodes
    nodes = workflow.get("nodes", [])
    node_types = []
    for node in nodes[:8]:  # Limit to first 8 nodes
        node_type = node.get("type", "")
        if "n8n-nodes-base." in node_type:
            node_types.append(node_type.replace("n8n-nodes-base.", ""))
    
    if node_types:
        parts.append(f"Nodes: {', '.join(node_types)}")
    
    # Get archetype if available
    if workflow.get("meta", {}).get("archetype"):
        parts.append(f"Archetype: {workflow['meta']['archetype']}")
    
    return " | ".join(parts)

def generate_names_batch(model, workflows: list) -> list:
    """Generate names for a batch of workflows."""
    # Create summaries
    summaries = []
    for i, wf in enumerate(workflows, 1):
        summary = extract_workflow_summary(wf)
        summaries.append(f"{i}. {summary}")
    
    prompt = PROMPT_TEMPLATE.format(workflows="\n".join(summaries))
    
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")
        
        # Parse response
        names = []
        for line in lines:
            # Remove numbering if present
            line = re.sub(r'^\d+[\.\)]\s*', '', line.strip())
            names.append(sanitize_filename(line))
        
        # Pad with defaults if not enough names
        while len(names) < len(workflows):
            names.append("unnamed_workflow")
        
        return names[:len(workflows)]
        
    except Exception as e:
        print(f"Error generating names: {e}")
        return ["unnamed_workflow"] * len(workflows)

def walk_dir(dir_path: Path) -> list:
    """Recursively get all JSON files."""
    files = []
    for item in dir_path.iterdir():
        if item.is_dir():
            files.extend(walk_dir(item))
        elif item.suffix == ".json":
            files.append(item)
    return files

def main():
    print("LLM Workflow Renaming with Gemini\n")
    
    # Configure Gemini
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY or GEMINI_API_KEY not set")
        return
    
    genai.configure(api_key=api_key)
    
    # Try primary model first
    try:
        model = genai.GenerativeModel(PRIMARY_MODEL)
        print(f"Using model: {PRIMARY_MODEL}")
    except:
        model = genai.GenerativeModel(FALLBACK_MODEL)
        print(f"Fallback to: {FALLBACK_MODEL}")
    
    # Collect files to process
    all_files = []
    for folder in FOLDERS_TO_PROCESS:
        folder_path = WORKFLOWS_DIR / folder
        if folder_path.exists():
            files = walk_dir(folder_path)
            # Filter to files needing renaming (hash names OR unnamed_workflow*)
            files = [f for f in files if re.match(r'^(unnamed_workflow.*|[a-f0-9]{8,})\.json$', f.name)]
            all_files.extend(files)
            print(f"Found {len(files)} files to rename in {folder}/")
    
    print(f"\nTotal files to rename: {len(all_files)}\n")
    
    if not all_files:
        print("No files need renaming!")
        return
    
    # Process in batches
    stats = {"renamed": 0, "errors": 0, "skipped": 0}
    used_names = set()
    
    with open(OUTPUT_LOG, 'a') as log_f:
        for i in range(0, len(all_files), BATCH_SIZE):
            batch_files = all_files[i:i + BATCH_SIZE]
            
            # Load workflows
            workflows = []
            for f in batch_files:
                try:
                    with open(f, 'r') as wf:
                        workflows.append(json.load(wf))
                except:
                    workflows.append({"name": f.stem})
            
            # Generate names
            new_names = generate_names_batch(model, workflows)
            
            # Rename files
            for j, (file_path, new_name) in enumerate(zip(batch_files, new_names)):
                # Handle duplicates
                base_name = new_name
                counter = 0
                while new_name in used_names:
                    counter += 1
                    new_name = f"{base_name}_{counter}"
                used_names.add(new_name)
                
                new_path = file_path.parent / f"{new_name}.json"
                
                try:
                    file_path.rename(new_path)
                    stats["renamed"] += 1
                    
                    # Log
                    log_f.write(json.dumps({
                        "old": str(file_path),
                        "new": str(new_path)
                    }) + "\n")
                    
                except Exception as e:
                    stats["errors"] += 1
                    print(f"Error renaming {file_path}: {e}")
            
            processed = min(i + BATCH_SIZE, len(all_files))
            print(f"Progress: {processed}/{len(all_files)} ({100*processed/len(all_files):.1f}%)")
            
            time.sleep(DELAY_BETWEEN_CALLS)
    
    print(f"\n=== COMPLETE ===")
    print(f"Renamed: {stats['renamed']}")
    print(f"Errors:  {stats['errors']}")
    print(f"\nNext: node scripts/generate-manifest.mjs")

if __name__ == "__main__":
    main()
