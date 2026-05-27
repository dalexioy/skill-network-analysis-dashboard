import pandas as pd
import networkx as nx
import community as community_louvain
import os
import json

# Δημιουργία φακέλου εξόδου αν δεν υπάρχει
output_folder = "data/quarterly_louvain_results"
os.makedirs(output_folder, exist_ok=True)

# Τα 4 διαθέσιμα τρίμηνα
quarters = ["2024Q1", "2024Q2", "2024Q3", "2024Q4"]

for quarter in quarters:
    file_path = f"data/temporal_edges_per_quarter/temporal_edges_{quarter}.csv"
    if not os.path.exists(file_path):
        print(f"⚠️ Δεν βρέθηκε αρχείο για {quarter}")
        continue

    print(f"🔄 Τρέχουμε Louvain για {quarter}...")

    # Φόρτωση δεδομένων ακμών
    df = pd.read_csv(file_path)
    G = nx.DiGraph()

    # Δημιουργία directed γράφου με βάρη
    for _, row in df.iterrows():
        src, tgt, w = row['source'], row['target'], row['weight']
        if G.has_edge(src, tgt):
            G[src][tgt]['weight'] += w
        else:
            G.add_edge(src, tgt, weight=w)

    # Υπολογισμός μετρικών για directed γράφο
    pagerank = nx.pagerank(G, weight='weight')
    degree_centrality = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G, weight='weight')
    in_degree = dict(G.in_degree(weight='weight'))
    out_degree = dict(G.out_degree(weight='weight'))
    density = nx.density(G)

    # Louvain απαιτεί undirected γράφο
    G_undirected = G.to_undirected()
    partition = community_louvain.best_partition(G_undirected, weight='weight')
    modularity = community_louvain.modularity(partition, G_undirected)

    # Δημιουργία λίστας κόμβων με μετρικές
    results = []
    for skill in G.nodes():
        results.append({
            "skill": skill,
            "quarter": quarter,
            "community": partition.get(skill, -1),
            "pagerank": pagerank.get(skill, 0.0),
            "degree_centrality": degree_centrality.get(skill, 0.0),
            "betweenness": betweenness.get(skill, 0.0),
            "in_degree": in_degree.get(skill, 0.0),
            "out_degree": out_degree.get(skill, 0.0),
            "density": density,
            "modularity": modularity
        })

    # Αποθήκευση κόμβων
    output_path = os.path.join(output_folder, f"louvain_{quarter}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✅ Αποθηκεύτηκε: {output_path}")

    # Αποθήκευση ακμών για visualisation
    edge_data = [
        {"source": u, "target": v, "weight": d['weight']}
        for u, v, d in G.edges(data=True)
    ]
    edge_output_path = os.path.join(output_folder, f"edges_{quarter}.json")
    with open(edge_output_path, "w", encoding="utf-8") as f:
        json.dump(edge_data, f, ensure_ascii=False, indent=2)
    print(f"📊 Αποθηκεύτηκαν και οι ακμές: {edge_output_path}")
