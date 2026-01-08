"""
Cluster workflows using embeddings to discover semantic categories.
Uses K-means clustering to group similar workflows.

Usage: python scripts/cluster-workflows.py
"""

import json
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from collections import Counter

# Configuration
EMBEDDINGS_FILE = Path(__file__).parent.parent / "embeddings_together.jsonl"
OUTPUT_FILE = Path(__file__).parent.parent / "workflow_clusters.json"
N_CLUSTERS = 25  # Number of semantic categories to discover
RANDOM_STATE = 42

# Suggested cluster names (will be refined based on actual content)
SUGGESTED_LABELS = [
    "AI Agents & Chat",
    "Data Sync & ETL",
    "CRM Automation",
    "Email & Notifications",
    "Social Media",
    "E-commerce",
    "Project Management",
    "Database Operations",
    "File Processing",
    "API Integrations",
    "Scheduling & Triggers",
    "Analytics & Reporting",
    "Document Processing",
    "Lead Generation",
    "Customer Support",
    "Backup & Recovery",
    "Monitoring & Alerts",
    "Content Management",
    "Form Processing",
    "Webhook Handlers",
    "Authentication & Security",
    "Calendar & Events",
    "Spreadsheet Automation",
    "Communication Tools",
    "Development & DevOps"
]

def main():
    print("Loading embeddings...")
    
    # Load embeddings
    records = []
    embeddings = []
    with open(EMBEDDINGS_FILE, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append({
                    'id': record.get('id'),
                    'name': record.get('name'),
                    'category': record.get('category')
                })
                embeddings.append(record['embedding'])
            except json.JSONDecodeError as e:
                print(f"Skipping line {line_num}: {e}")
                continue
    
    print(f"Loaded {len(embeddings)} embeddings")
    
    # Convert to numpy array and normalize
    X = np.array(embeddings)
    X = normalize(X)  # L2 normalization for cosine similarity
    
    print(f"Running K-means with {N_CLUSTERS} clusters...")
    
    # Run K-means
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=RANDOM_STATE, n_init=10, verbose=1)
    labels = kmeans.fit_predict(X)
    
    # Analyze clusters
    print("\n=== CLUSTER ANALYSIS ===\n")
    
    cluster_info = {}
    for cluster_id in range(N_CLUSTERS):
        # Get workflows in this cluster
        indices = np.where(labels == cluster_id)[0]
        cluster_records = [records[i] for i in indices]
        
        # Count categories in this cluster
        category_counts = Counter(r['category'] for r in cluster_records)
        
        # Get sample names
        sample_names = [r['name'] for r in cluster_records[:5]]
        
        # Assign a label (use suggestion if available, otherwise generic)
        suggested_label = SUGGESTED_LABELS[cluster_id] if cluster_id < len(SUGGESTED_LABELS) else f"Category {cluster_id}"
        
        cluster_info[cluster_id] = {
            'label': suggested_label,
            'count': len(indices),
            'top_categories': dict(category_counts.most_common(3)),
            'sample_names': sample_names
        }
        
        print(f"Cluster {cluster_id}: {suggested_label}")
        print(f"  Count: {len(indices)}")
        print(f"  Top categories: {dict(category_counts.most_common(3))}")
        print(f"  Samples: {sample_names[:3]}")
        print()
    
    # Create output with cluster assignments
    output = {
        'n_clusters': N_CLUSTERS,
        'cluster_info': cluster_info,
        'assignments': {}
    }
    
    for i, record in enumerate(records):
        cluster_id = int(labels[i])
        workflow_id = record.get('id') or record.get('name')
        output['assignments'][workflow_id] = {
            'cluster': cluster_id,
            'label': cluster_info[cluster_id]['label']
        }
    
    # Save results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to: {OUTPUT_FILE}")
    print("\nNext steps:")
    print("1. Review cluster assignments")
    print("2. Refine cluster labels based on content")
    print("3. Apply labels to workflow files")

if __name__ == "__main__":
    main()
