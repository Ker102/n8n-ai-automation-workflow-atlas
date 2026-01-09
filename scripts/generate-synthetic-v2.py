"""
Node-swap synthetic generation from archetypes.
Generates new workflows by swapping compatible nodes while preserving connections.

Usage: python scripts/generate-synthetic-v2.py
"""

import json
import random
from pathlib import Path
from copy import deepcopy

# Configuration
ARCHETYPES_DIR = Path(__file__).parent.parent / "archetypes"
OUTPUT_DIR = Path(__file__).parent.parent / "workflows" / "synthetic_v2"
VARIATIONS_PER_ARCHETYPE = 1000  # Target: 100 archetypes × 1000 = 100k workflows
RANDOM_SEED = 42

# Node swap mappings - compatible replacements
NODE_SWAPS = {
    # Triggers
    "webhook": ["httpRequest", "formTrigger", "manualTrigger"],
    "manualTrigger": ["scheduleTrigger", "cronTrigger", "webhook"],
    "scheduleTrigger": ["cronTrigger", "manualTrigger"],
    "emailTrigger": ["imapEmail", "gmailTrigger"],
    "gmailTrigger": ["emailTrigger", "microsoftOutlookTrigger"],
    
    # Databases
    "postgres": ["mysql", "mssql", "mariaDb", "mongoDb"],
    "mysql": ["postgres", "mssql", "mariaDb"],
    "mongoDb": ["postgres", "mysql", "redis"],
    "redis": ["mongoDb", "postgres"],
    "airtable": ["googleSheets", "notion", "baserow", "nocodb"],
    "googleSheets": ["airtable", "notion", "baserow"],
    "notion": ["airtable", "googleSheets", "clickup"],
    
    # Communication
    "slack": ["discord", "mattermost", "microsoftTeams", "telegram"],
    "discord": ["slack", "mattermost", "telegram"],
    "telegram": ["slack", "discord", "whatsapp"],
    "email": ["gmail", "microsoftOutlook", "sendgrid"],
    "gmail": ["email", "microsoftOutlook"],
    
    # CRM
    "hubspot": ["salesforce", "pipedrive", "zoho"],
    "salesforce": ["hubspot", "pipedrive"],
    "pipedrive": ["hubspot", "salesforce", "airtable"],
    
    # Project Management
    "trello": ["asana", "clickup", "jira", "monday"],
    "asana": ["trello", "clickup", "jira"],
    "jira": ["asana", "trello", "linear", "github"],
    "clickup": ["asana", "trello", "notion"],
    
    # Storage
    "googleDrive": ["dropbox", "oneDrive", "box"],
    "dropbox": ["googleDrive", "oneDrive"],
    "s3": ["googleCloudStorage", "azureBlob"],
    
    # AI
    "openAi": ["anthropic", "googleAi", "ollama"],
    "anthropic": ["openAi", "googleAi"],
}

def get_swap_candidates(node_type):
    """Get compatible replacement nodes."""
    base_type = node_type.replace("n8n-nodes-base.", "").replace("Trigger", "").lower()
    
    for key, swaps in NODE_SWAPS.items():
        if key.lower() in base_type or base_type in key.lower():
            return swaps
    return []

def swap_node(node, swap_to):
    """Create a swapped version of a node."""
    new_node = deepcopy(node)
    old_type = node.get("type", "")
    
    # Preserve trigger status
    is_trigger = "trigger" in old_type.lower()
    new_type = f"n8n-nodes-base.{swap_to}"
    if is_trigger and "trigger" not in swap_to.lower():
        new_type = f"n8n-nodes-base.{swap_to}Trigger"
    
    new_node["type"] = new_type
    
    # Update name
    old_name = node.get("name", "")
    new_node["name"] = old_name.replace(old_type.split(".")[-1], swap_to)
    
    return new_node

def generate_variations(archetype, count):
    """Generate variations of an archetype by node swapping."""
    variations = []
    nodes = archetype.get("nodes", [])
    
    # Find swappable nodes
    swappable = []
    for i, node in enumerate(nodes):
        node_type = node.get("type", "")
        candidates = get_swap_candidates(node_type)
        if candidates:
            swappable.append((i, candidates))
    
    if not swappable:
        return []
    
    for v in range(count):
        new_wf = deepcopy(archetype)
        
        # Randomly swap 1-3 nodes
        num_swaps = random.randint(1, min(3, len(swappable)))
        to_swap = random.sample(swappable, num_swaps)
        
        for node_idx, candidates in to_swap:
            swap_to = random.choice(candidates)
            new_wf["nodes"][node_idx] = swap_node(nodes[node_idx], swap_to)
        
        # Update workflow name
        original_name = archetype.get("name", "Workflow")
        new_wf["name"] = f"{original_name}_v{v+1}"
        
        # Add generation metadata
        if "meta" not in new_wf:
            new_wf["meta"] = {}
        new_wf["meta"]["generated"] = True
        new_wf["meta"]["sourceArchetype"] = archetype.get("name", "unknown")
        
        variations.append(new_wf)
    
    return variations

def main():
    random.seed(RANDOM_SEED)
    print("Generating synthetic workflows from archetypes...\n")
    
    # Load archetypes
    archetypes = []
    for category_dir in ARCHETYPES_DIR.iterdir():
        if category_dir.is_dir():
            for archetype_file in category_dir.glob("*.json"):
                try:
                    archetype = json.loads(archetype_file.read_text())
                    archetypes.append((category_dir.name, archetype_file.name, archetype))
                except:
                    pass
    
    print(f"Loaded {len(archetypes)} archetypes\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    total_generated = 0
    for category, filename, archetype in archetypes:
        variations = generate_variations(archetype, VARIATIONS_PER_ARCHETYPE)
        
        if not variations:
            print(f"  {category}/{filename}: No swappable nodes")
            continue
        
        # Save variations
        cat_dir = OUTPUT_DIR / category
        cat_dir.mkdir(exist_ok=True)
        
        base_name = filename.replace(".json", "")
        for i, wf in enumerate(variations):
            out_path = cat_dir / f"{base_name}_var{i+1}.json"
            out_path.write_text(json.dumps(wf, indent=2))
            total_generated += 1
        
        print(f"  {category}: Generated {len(variations)} from {filename[:30]}")
    
    print(f"\n=== COMPLETE ===")
    print(f"Total generated: {total_generated}")
    print(f"Saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
