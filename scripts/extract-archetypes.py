"""
Extract high-quality archetypes from semantic clusters.
Selects the best workflows per cluster based on:
- Connection skeleton (nodes are connected)
- Node diversity
- Complexity

Usage: python scripts/extract-archetypes.py
"""

import json
from pathlib import Path
from collections import defaultdict

# Configuration
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"
CLUSTERS_FILE = Path(__file__).parent.parent / "workflow_clusters.json"
OUTPUT_DIR = Path(__file__).parent.parent / "archetypes"
ARCHETYPES_PER_CLUSTER = 4  # Target 4 archetypes per cluster = ~100 total
MIN_NODES = 3
MIN_CONNECTIONS = 2

def walk_dir(dir_path):
    """Recursively get all JSON files."""
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
    if not connections or len(connections) == 0:
        return False
    
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
    
    nodes = workflow.get("nodes", [])
    if len(nodes) < MIN_NODES:
        return False
    
    # At least 50% of nodes should be connected
    return len(connected_nodes) >= len(nodes) * 0.5

def score_workflow(workflow, file_path):
    """Score workflow quality for archetype selection."""
    score = 0
    
    nodes = workflow.get("nodes", [])
    connections = workflow.get("connections", {})
    
    # Node count (prefer moderate complexity)
    node_count = len(nodes)
    if 4 <= node_count <= 10:
        score += 30
    elif 10 < node_count <= 20:
        score += 20
    elif node_count > 20:
        score += 10
    else:
        score += 5
    
    # Connection count
    conn_count = sum(len(v.get("main", [])) for v in connections.values())
    score += min(conn_count * 5, 30)
    
    # Node diversity (unique node types)
    node_types = set()
    for node in nodes:
        node_type = node.get("type", "")
        if "n8n-nodes-base." in node_type:
            node_types.add(node_type.replace("n8n-nodes-base.", ""))
    score += min(len(node_types) * 5, 25)
    
    # Has trigger node
    has_trigger = any("trigger" in n.get("type", "").lower() for n in nodes)
    if has_trigger:
        score += 15
    
    # Has name and description
    if workflow.get("name"):
        score += 5
    if workflow.get("description"):
        score += 5
    
    return score

def main():
    print("Extracting archetypes from semantic clusters...\n")
    
    # Load cluster assignments
    clusters_data = json.loads(CLUSTERS_FILE.read_text())
    assignments = clusters_data.get("assignments", {})
    cluster_info = clusters_data.get("cluster_info", {})
    
    print(f"Loaded {len(assignments)} cluster assignments")
    print(f"Found {len(cluster_info)} clusters\n")
    
    # Group files by cluster
    cluster_files = defaultdict(list)
    all_files = walk_dir(WORKFLOWS_DIR)
    
    print(f"Scanning {len(all_files)} workflow files...")
    
    for file_path in all_files:
        file_id = file_path.stem.lower()
        if file_id in assignments:
            cluster_id = assignments[file_id]["cluster"]
            cluster_files[cluster_id].append(file_path)
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Extract archetypes from each cluster
    total_archetypes = 0
    stats = {"valid": 0, "invalid": 0}
    
    for cluster_id in sorted(cluster_info.keys(), key=int):
        info = cluster_info[cluster_id]
        label = info["label"]
        files = cluster_files.get(int(cluster_id), [])
        
        print(f"\nCluster {cluster_id}: {label} ({len(files)} files)")
        
        # Score and filter workflows
        candidates = []
        for file_path in files[:200]:  # Check up to 200 per cluster
            try:
                workflow = json.loads(file_path.read_text())
                if has_valid_skeleton(workflow):
                    score = score_workflow(workflow, file_path)
                    candidates.append((score, file_path, workflow))
                    stats["valid"] += 1
                else:
                    stats["invalid"] += 1
            except Exception as e:
                stats["invalid"] += 1
        
        # Select top archetypes
        candidates.sort(reverse=True, key=lambda x: x[0])
        selected = candidates[:ARCHETYPES_PER_CLUSTER]
        
        # Save archetypes
        cluster_dir = OUTPUT_DIR / f"cluster_{cluster_id}_{label.replace(' ', '_').replace('&', 'and')}"
        cluster_dir.mkdir(exist_ok=True)
        
        for i, (score, file_path, workflow) in enumerate(selected):
            archetype_path = cluster_dir / f"archetype_{i+1}_{file_path.stem[:30]}.json"
            archetype_path.write_text(json.dumps(workflow, indent=2))
            total_archetypes += 1
            print(f"  → {file_path.stem[:40]}... (score: {score})")
    
    print(f"\n=== EXTRACTION COMPLETE ===")
    print(f"Total archetypes: {total_archetypes}")
    print(f"Valid workflows checked: {stats['valid']}")
    print(f"Invalid (no skeleton): {stats['invalid']}")
    print(f"\nArchetypes saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
