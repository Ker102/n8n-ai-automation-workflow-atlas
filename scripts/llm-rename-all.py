"""
LLM-based workflow naming using Gemini API - Full Rename v2
Generates descriptive names for ALL workflows using semantic labels.

Usage:
  GOOGLE_API_KEY=xxx python scripts/llm-rename-all.py
"""

import json
import os
import time
import re
from pathlib import Path
import google.generativeai as genai

# Configuration
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
FOLDERS_TO_PROCESS = ["synthetic", "external", "ai-automation-lab", "initial_megapack"]
OUTPUT_LOG = Path(__file__).parent.parent / "rename_all_log.jsonl"
BATCH_SIZE = 15  # Workflows per API call
DELAY_BETWEEN_CALLS = 0.3  # seconds
MODEL_NAME = "gemini-2.0-flash"

# Prompt template with semantic context
PROMPT_TEMPLATE = """You are naming n8n automation workflows. Generate a short, descriptive filename for each.

Rules:
- snake_case (lowercase with underscores)
- Max 45 characters
- Focus on ACTION + CONTEXT (what it does, not just tools)
- Include the semantic category naturally
- No file extension

Examples:
- ai_agent_slack_ticket_triage
- daily_crm_sync_hubspot_to_sheets
- email_lead_followup_automation
- weekly_sales_report_generator

Workflows:
{workflows}

New names (one per line, no numbers):"""

def sanitize_filename(name: str) -> str:
    """Clean up generated name to be a valid filename."""
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9_]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')[:45]
    return name or "unnamed_workflow"

def extract_workflow_summary(workflow: dict, file_path: Path) -> str:
    """Create a rich summary with semantic label."""
    parts = []
    
    # Semantic label (most important!)
    meta = workflow.get("meta", {})
    if meta.get("semanticLabel"):
        parts.append(f"Category: {meta['semanticLabel']}")
    
    # Complexity
    if meta.get("complexity"):
        parts.append(f"Complexity: {meta['complexity']}")
    
    # Workflow name
    name = workflow.get("name", file_path.stem)
    parts.append(f"Name: {name[:60]}")
    
    # Key nodes/integrations
    nodes = workflow.get("nodes", [])
    node_types = set()
    for node in nodes[:10]:
        node_type = node.get("type", "")
        if "n8n-nodes-base." in node_type:
            node_types.add(node_type.replace("n8n-nodes-base.", ""))
    if node_types:
        parts.append(f"Tools: {', '.join(sorted(node_types)[:5])}")
    
    return " | ".join(parts)

def generate_names_batch(model, workflows: list, file_paths: list) -> list:
    """Generate names for a batch of workflows."""
    summaries = []
    for i, (wf, fp) in enumerate(zip(workflows, file_paths), 1):
        summary = extract_workflow_summary(wf, fp)
        summaries.append(f"{i}. {summary}")
    
    prompt = PROMPT_TEMPLATE.format(workflows="\n".join(summaries))
    
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")
        
        names = []
        for line in lines:
            line = re.sub(r'^\d+[\.\)]\s*', '', line.strip())
            if line and not line.startswith('-'):
                names.append(sanitize_filename(line))
        
        # Pad with fallbacks if needed
        while len(names) < len(workflows):
            names.append(sanitize_filename(file_paths[len(names)].stem[:30]))
        
        return names[:len(workflows)]
        
    except Exception as e:
        print(f"Error: {e}")
        return [sanitize_filename(fp.stem[:30]) for fp in file_paths]

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
    print("LLM Full Workflow Renaming with Gemini\n")
    
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not set")
        return
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)
    print(f"Using model: {MODEL_NAME}")
    
    # Collect all files
    all_files = []
    for folder in FOLDERS_TO_PROCESS:
        folder_path = WORKFLOWS_DIR / folder
        if folder_path.exists():
            files = walk_dir(folder_path)
            all_files.extend(files)
            print(f"Found {len(files)} files in {folder}/")
    
    print(f"\nTotal files to rename: {len(all_files)}\n")
    
    if not all_files:
        print("No files found!")
        return
    
    # Process in batches
    stats = {"renamed": 0, "errors": 0, "skipped": 0}
    used_names = set()
    
    with open(OUTPUT_LOG, 'w') as log_f:
        for i in range(0, len(all_files), BATCH_SIZE):
            batch_files = all_files[i:i + BATCH_SIZE]
            
            # Load workflows
            workflows = []
            valid_files = []
            for f in batch_files:
                try:
                    with open(f, 'r') as wf:
                        workflows.append(json.load(wf))
                        valid_files.append(f)
                except:
                    stats["errors"] += 1
            
            if not workflows:
                continue
            
            # Generate names
            new_names = generate_names_batch(model, workflows, valid_files)
            
            # Rename files
            for file_path, new_name in zip(valid_files, new_names):
                # Handle duplicates
                base_name = new_name
                counter = 0
                while new_name in used_names:
                    counter += 1
                    new_name = f"{base_name}_{counter}"
                used_names.add(new_name)
                
                new_path = file_path.parent / f"{new_name}.json"
                
                if new_path == file_path:
                    stats["skipped"] += 1
                    continue
                
                try:
                    file_path.rename(new_path)
                    stats["renamed"] += 1
                    log_f.write(json.dumps({"old": str(file_path), "new": str(new_path)}) + "\n")
                except Exception as e:
                    stats["errors"] += 1
            
            processed = min(i + BATCH_SIZE, len(all_files))
            if processed % 500 == 0 or processed == len(all_files):
                print(f"Progress: {processed}/{len(all_files)} ({100*processed/len(all_files):.1f}%)")
            
            time.sleep(DELAY_BETWEEN_CALLS)
    
    print(f"\n=== COMPLETE ===")
    print(f"Renamed: {stats['renamed']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Errors:  {stats['errors']}")
    print(f"\nNext: node scripts/generate-manifest.mjs")

if __name__ == "__main__":
    main()
