"""
Quality filter for workflows - validates connection skeleton and structure.
Prepares high-quality dataset for RAG and fine-tuning.

Usage: python scripts/quality-filter.py
"""

import json
from pathlib import Path
from collections import defaultdict

# Configuration
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
OUTPUT_DIR = Path(__file__).parent.parent / "rag_dataset"
MIN_NODES = 3
MIN_CONNECTIONS = 2

def walk_dir(dir_path):
    files = []
    for item in dir_path.iterdir():
        if item.is_dir():
            files.extend(walk_dir(item))
        elif item.suffix == ".json":
            files.append(item)
    return files

def validate_workflow(workflow):
    """Validate workflow has proper structure and connections."""
    nodes = workflow.get("nodes", [])
    connections = workflow.get("connections", {})
    
    # Must have minimum nodes
    if len(nodes) < MIN_NODES:
        return False, "too_few_nodes"
    
    # Must have connections
    if not connections or len(connections) < MIN_CONNECTIONS:
        return False, "no_connections"
    
    # Count connected nodes
    connected_nodes = set()
    for source, data in connections.items():
        connected_nodes.add(source)
        main = data.get("main", [])
        for outputs in main:
            if isinstance(outputs, list):
                for conn in outputs:
                    if isinstance(conn, dict) and "node" in conn:
                        connected_nodes.add(conn["node"])
    
    # At least 60% of nodes connected
    if len(connected_nodes) < len(nodes) * 0.6:
        return False, "orphan_nodes"
    
    # Must have at least one trigger
    has_trigger = any("trigger" in n.get("type", "").lower() for n in nodes)
    if not has_trigger:
        return False, "no_trigger"
    
    # Valid JSON structure
    try:
        json.dumps(workflow)
    except:
        return False, "invalid_json"
    
    return True, "valid"

def score_workflow(workflow):
    """Score workflow quality (0-100)."""
    score = 50  # Base score
    nodes = workflow.get("nodes", [])
    connections = workflow.get("connections", {})
    
    # Node diversity
    node_types = set(n.get("type", "") for n in nodes)
    score += min(len(node_types) * 3, 15)
    
    # Connection complexity
    total_conns = sum(len(v.get("main", [])) for v in connections.values())
    score += min(total_conns * 2, 15)
    
    # Has description/name
    if workflow.get("name"):
        score += 5
    if workflow.get("description"):
        score += 5
    
    # Moderate complexity bonus
    if 5 <= len(nodes) <= 12:
        score += 10
    
    return min(score, 100)

def create_training_example(workflow, file_path):
    """Create instruction/response pair for fine-tuning."""
    nodes = workflow.get("nodes", [])
    node_types = []
    for n in nodes:
        nt = n.get("type", "").replace("n8n-nodes-base.", "")
        if nt:
            node_types.append(nt)
    
    # Generate instruction from workflow
    name = workflow.get("name", file_path.stem)
    category = workflow.get("meta", {}).get("semanticLabel", "automation")
    
    instruction = f"Create an n8n workflow for: {name}"
    if category:
        instruction += f" (Category: {category})"
    if node_types:
        instruction += f" using {', '.join(node_types[:5])}"
    
    return {
        "instruction": instruction,
        "output": json.dumps(workflow),
        "category": category,
        "score": score_workflow(workflow)
    }

def main():
    print("Filtering workflows for quality...\n")
    
    all_files = walk_dir(WORKFLOWS_DIR)
    print(f"Scanning {len(all_files)} workflow files...\n")
    
    stats = defaultdict(int)
    high_quality = []
    
    for i, file_path in enumerate(all_files):
        if i % 10000 == 0:
            print(f"Progress: {i}/{len(all_files)}")
        
        try:
            workflow = json.loads(file_path.read_text())
            valid, reason = validate_workflow(workflow)
            
            if valid:
                score = score_workflow(workflow)
                if score >= 60:  # High quality threshold
                    high_quality.append((score, file_path, workflow))
                    stats["high_quality"] += 1
                else:
                    stats["low_score"] += 1
            else:
                stats[reason] += 1
        except:
            stats["parse_error"] += 1
    
    print(f"\n=== VALIDATION RESULTS ===")
    for key, count in sorted(stats.items()):
        print(f"  {key}: {count}")
    
    # Sort by score and save high quality
    high_quality.sort(reverse=True, key=lambda x: x[0])
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Save as JSONL for training
    training_file = OUTPUT_DIR / "training_data.jsonl"
    with open(training_file, 'w') as f:
        for score, file_path, workflow in high_quality:
            example = create_training_example(workflow, file_path)
            f.write(json.dumps(example) + "\n")
    
    # Save high quality workflows
    workflows_file = OUTPUT_DIR / "high_quality_workflows.jsonl"
    with open(workflows_file, 'w') as f:
        for score, file_path, workflow in high_quality:
            f.write(json.dumps({"score": score, "path": str(file_path), "workflow": workflow}) + "\n")
    
    print(f"\n=== COMPLETE ===")
    print(f"High quality workflows: {len(high_quality)}")
    print(f"Saved to: {OUTPUT_DIR}")
    print(f"  - training_data.jsonl (for fine-tuning)")
    print(f"  - high_quality_workflows.jsonl (for RAG)")

if __name__ == "__main__":
    main()
