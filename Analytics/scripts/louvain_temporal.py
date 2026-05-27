import os
import json
import pandas as pd
import networkx as nx
import community
from tqdm import tqdm
from collections import defaultdict

input_folder = "data/temporal_edges_per_quarter/"
output_json_folder = "data/temporal_louvain_results/"
output_stats_folder = "data/temporal_louvain_stats/"
os.makedirs(output_json_folder, exist_ok=True)
os.makedirs(output_stats_folder, exist_ok=True)

for filename in tqdm(os.listdir(input_folder)):
    if not filename.endswith(".csv"):
        continue

    quarter = filename.replace(".csv", "").split("_")[-1]
    filepath = os.path.join(input_folder, filename)
    df = pd.read_csv(filepath)
    df = df[df["source"] != df["target"]]

    # Directed graph
    G = nx.from_pandas_edgelist(df, source="source", target="target", edge_attr="weight", create_using=nx.DiGraph())

    # Louvain (on undirected)
    G_undirected = G.to_undirected()
    partition = community.best_partition(G_undirected)
    nx.set_node_attributes(G, partition, "community")

    # Centralities
    pagerank = nx.pagerank(G)
    betweenness = nx.betweenness_centrality(G, k=None)
    degree = dict(G.degree())

    # Αναλυτικά ανά skill
    skill_results = []
    for node in G.nodes():
        skill_results.append({
            "quarter": quarter,
            "skill": node,
            "community": partition[node],
            "pagerank": round(pagerank.get(node, 0), 6),
            "betweenness": round(betweenness.get(node, 0), 6),
            "degree": round(degree.get(node, 0), 6)
        })

    # Αποθήκευση ανα skill
    with open(os.path.join(output_json_folder, f"temporal_louvain_{quarter}.json"), "w", encoding="utf-8") as f:
        json.dump(skill_results, f, indent=2, ensure_ascii=False)

    # ---- Κοινοτικά Στατιστικά ----
    df_nodes = pd.DataFrame(skill_results)
    df_edges = pd.DataFrame({
        "source": [e[0] for e in G.edges()],
        "target": [e[1] for e in G.edges()]
    })

    # Group by community
    stats = []
    for community_id in sorted(df_nodes["community"].unique()):
        members = df_nodes[df_nodes["community"] == community_id]
        n_nodes = len(members)

        subgraph = G.subgraph(members["skill"].tolist()).copy()
        n_edges = subgraph.number_of_edges()
        density = nx.density(subgraph)
        avg_degree = members["degree"].mean()
        avg_pagerank = members["pagerank"].mean()
        avg_betweenness = members["betweenness"].mean()

        stats.append({
            "quarter": quarter,
            "community": community_id,
            "n_skills": n_nodes,
            "n_edges": n_edges,
            "density": round(density, 4),
            "avg_degree": round(avg_degree, 4),
            "avg_pagerank": round(avg_pagerank, 4),
            "avg_betweenness": round(avg_betweenness, 4)
        })

    df_stats = pd.DataFrame(stats)
    df_stats.to_csv(os.path.join(output_stats_folder, f"community_metrics_{quarter}.csv"), index=False)

print("✅ Ολοκληρώθηκε Louvain + Community Stats για όλα τα τρίμηνα.")
