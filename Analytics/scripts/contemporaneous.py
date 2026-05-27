import pandas as pd
import networkx as nx
import json
from collections import defaultdict
import os

# 🔁 Τρίμηνα
quarters = ["2024Q1", "2024Q2", "2024Q3", "2024Q4"]
edge_folder = "data/contemporaneous_edges_per_quarter/"
json_path = "data/contemporaneous.json"

# 📥 Φόρτωση global community από JSON
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

skill_to_comm = {entry["skill"]: entry["community"] for entry in data}
skill_to_label = {entry["skill"]: entry["community_label"] for entry in data}

# 📊 Αποτελέσματα
results = []

for quarter in quarters:
    edge_file = os.path.join(edge_folder, f"contemporaneous_edges_{quarter}.csv")
    if not os.path.exists(edge_file):
        continue

    print(f"🔎 Quarter: {quarter}")
    df_edges = pd.read_csv(edge_file)

    # Φιλτράρισμα edges για skills του global community
    df_edges = df_edges[df_edges["source"].isin(skill_to_comm) & df_edges["target"].isin(skill_to_comm)]

    # Φτιάχνουμε γράφο
    G = nx.from_pandas_edgelist(df_edges, source="source", target="target", edge_attr="weight")

    # 🔄 Ομαδοποίηση skills σε κοινότητες βάσει global Louvain
    comm_to_nodes = defaultdict(list)
    for node in G.nodes():
        comm = skill_to_comm.get(node)
        if comm is not None:
            comm_to_nodes[comm].append(node)

    # 📊 Μετρικές ανά κοινότητα
    for comm, nodes in comm_to_nodes.items():
        subG = G.subgraph(nodes)
        n = subG.number_of_nodes()
        e = subG.number_of_edges()
        degs = [subG.degree(n) for n in nodes]

        # Αποθήκευση
        results.append({
            "quarter": quarter,
            "community": comm,
            "community_label": skill_to_label.get(nodes[0], "Unknown"),
            "n_skills": n,
            "n_edges": e,
            "density": round(nx.density(subG), 4) if n > 1 else 0,
            "avg_degree": round(sum(degs) / n, 3) if n > 0 else 0
        })

# 💾 Αποθήκευση
df_stats = pd.DataFrame(results)
os.makedirs("data/results", exist_ok=True)
df_stats.to_csv("data/results/contemporaneous_stats_global_communities_per_quarter.csv", index=False)

print("✅ Ολοκληρώθηκε: data/results/contemporaneous_stats_global_communities_per_quarter.csv")
