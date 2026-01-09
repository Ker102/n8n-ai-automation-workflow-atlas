"""
Extract archetypes using semanticLabel from workflow meta.
Scans all workflows and groups by their embedded semantic label.

Usage: python scripts/extract-archetypes-v2.py
"""

import json
from pathlib import Path
from collections import defaultdict

# Configuration
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
OUTPUT_DIR = Path(__file__).parent.parent / "archetypes"
ARCHETYPES_PER_CATEGORY = 4
MIN_NODES = 3

def walk_dir(dir_path):
    files = []
    for item in dir_path.iterdir():
        if item.is_dir():
            files.extend(walk_dir(item))
        elif item.suffix == ".json":
            files.append(item)
    return files

def has_valid_skeleton(workflow):
    """Check if workflow has valid node connections."""
    connections = workflow.get("connections", {})
    if not connections:
        return False
    
    connected_nodes = set()
    for source, data in connections.items():
        connected_nodes.add(source)
        main = data.get("main", [])
        for outputs in main:
            if isinstance(outputs, list):
                for conn in outputs:
                    if isinstance(conn, dict) and "node" in conn:
                        connected_nodes.add(conn["node"])
    
    nodes = workflow.get("nodes", [])
    if len(nodes) < MIN_NODES:
        return False
    
    return len(connected_nodes) >= len(nodes) * 0.5

def score_workflow(workflow):
    score = 0
    nodes = workflow.get("nodes", [])
    connections = workflow.get("connections", {})
    
    # Node count
    node_count = len(nodes)
    if 4 <= node_count <= 10:
        score += 30
    elif 10 < node_count <= 20:
        score += 25
    elif node_count > 20:
        score += 15
    
    # Connections
    conn_count = sum(len(v.get("main", [])) for v in connections.values())
    score += min(conn_count * 5, 30)
    
    # Node diversity
    node_types = set()
    for node in nodes:
        nt = node.get("type", "")
        if "n8n-nodes-base." in nt:
            node_types.add(nt.replace("n8n-nodes-base.", ""))
    score += min(len(node_types) * 5, 25)
    
    # Trigger
    if any("trigger" in n.get("type", "").lower() for n in nodes):
        score += 15
    
    return score

def main():
    print("Extracting archetypes by semanticLabel...\n")
    
    all_files = walk_dir(WORKFLOWS_DIR)
    print(f"Scanning {len(all_files)} workflow files...\n")
    
    # Group by semantic label
    by_category = defaultdict(list)
    stats = {"valid": 0, "invalid": 0, "no_label": 0}
    
    for i, file_path in enumerate(all_files):
        if i % 5000 == 0:
            print(f"Progress: {i}/{len(all_files)}")
        
        try:
            workflow = json.loads(file_path.read_text())
            label = workflow.get("meta", {}).get("semanticLabel")
            
            if not label:
                stats["no_label"] += 1
                continue
            
            if has_valid_skeleton(workflow):
                score = score_workflow(workflow)
                by_category[label].append((score, file_path, workflow))
                stats["valid"] += 1
            else:
                stats["invalid"] += 1
        except:
            stats["invalid"] += 1
    
    print(f"\nFound {len(by_category)} semantic categories")
    
    # Create output
    OUTPUT_DIR.mkdir(exist_ok=True)
    total = 0
    
    for label in sorted(by_category.keys()):
        candidates = by_category[label]
        candidates.sort(reverse=True, key=lambda x: x[0])
        selected = candidates[:ARCHETYPES_PER_CATEGORY]
        
        safe_label = label.replace(" ", "_").replace("&", "and").replace("/", "_")
        cat_dir = OUTPUT_DIR / safe_label
        cat_dir.mkdir(exist_ok=True)
        
        print(f"\n{label} ({len(candidates)} valid)")
        for i, (score, fp, wf) in enumerate(selected):
            out_path = cat_dir / f"archetype_{i+1}_{fp.stem[:25]}.json"
            out_path.write_text(json.dumps(wf, indent=2))
            total += 1
            print(f"  → {fp.stem[:40]}... (score: {score})")
    
    print(f"\n=== COMPLETE ===")
    print(f"Total archetypes: {total}")
    print(f"Valid: {stats['valid']}, Invalid: {stats['invalid']}, No label: {stats['no_label']}")
    print(f"Saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
