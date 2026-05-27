import json
import pandas as pd

# Ορισμός paths
quarter = "2024Q4"
nodes_path = f"data/quarterly_louvain_results/enriched_louvain_{quarter}.json"
edges_path = f"data/temporal_edges_per_quarter/temporal_edges_{quarter}.csv"
output_path = f"data/quarterly_networks/{quarter}_network.json"

# Φόρτωση nodes (με Louvain μετρικές)
with open(nodes_path, "r") as f:
    nodes_data = json.load(f)

# Φόρτωση edges (source, target, weight)
edges_df = pd.read_csv(edges_path)

# Φιλτράρισμα edges με βάση τα skills που υπάρχουν στα nodes
valid_skills = set(node["skill"] for node in nodes_data)
filtered_edges = edges_df[
    (edges_df["source"].isin(valid_skills)) &
    (edges_df["target"].isin(valid_skills))
]

# Δημιουργία nodes για JSON
nodes_json = []
for node in nodes_data:
    nodes_json.append({
        "id": node["skill"],
        "community": node["community"],
        "community_label": node.get("community_label", ""),
        "pagerank": node["pagerank"],
        "betweenness": node["betweenness"],
        "degree": node["degree_centrality"],
        "in_degree": node["in_degree"],
        "out_degree": node["out_degree"]
    })

# Δημιουργία edges για JSON
edges_json = []
for _, row in filtered_edges.iterrows():
    edges_json.append({
        "source": row["source"],
        "target": row["target"],
        "weight": row.get("weight", 1)
    })

# Τελικό δίκτυο
network_json = {
    "nodes": nodes_json,
    "edges": edges_json
}

# Αποθήκευση
with open(output_path, "w") as f:
    json.dump(network_json, f, indent=2)

print(f"✅ Network file saved: {output_path}")
