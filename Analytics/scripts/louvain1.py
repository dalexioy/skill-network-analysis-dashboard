import pandas as pd
import networkx as nx
from glob import glob
from collections import defaultdict
import community as community_louvain  # python-louvain
import matplotlib.pyplot as plt
import json

# Βήμα 1: Διάβασμα όλων των temporal edges αρχείων (όλων των τριμήνων)
all_files = glob("data/temporal_edges_per_quarter/temporal_edges_*.csv")
df_all = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)

# Βήμα 2: Δημιουργία ενός directed γράφου με τα συνολικά temporal edges
G = nx.DiGraph()
for _, row in df_all.iterrows():
    src, tgt, w = row['source'], row['target'], row['weight']
    if G.has_edge(src, tgt):
        G[src][tgt]['weight'] += w
    else:
        G.add_edge(src, tgt, weight=w)

# Βήμα 3: Louvain community detection (πρέπει να είναι undirected)
G_undirected = G.to_undirected()
partition = community_louvain.best_partition(G_undirected, weight='weight')

# Βήμα 4: Ανάθεση community σε κάθε κόμβο
nx.set_node_attributes(G, partition, name="community")

# Βήμα 5: Εξαγωγή των skill-to-community δεδομένων
skill_communities = []
for node in G.nodes(data=True):
    skill = node[0]
    comm = node[1]['community']
    skill_communities.append({'skill': skill, 'community': comm})

df_skill_comms = pd.DataFrame(skill_communities)

# Βήμα 6: Αποθήκευση ως CSV και JSON
df_skill_comms.to_csv("data/temporal_louvain_skill_communities.csv", index=False)

with open("data/temporal_louvain_skill_communities.json", "w", encoding="utf-8") as f:
    json.dump(skill_communities, f, ensure_ascii=False, indent=2)

