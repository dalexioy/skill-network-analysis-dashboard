import pandas as pd
import networkx as nx
from tqdm import tqdm
import os

# 1. Φόρτωσε τα δεδομένα
df = pd.read_csv("data/new_clean_data.csv", usecols=["oja_id", "occupation4d", "last_active_date", "skill"])
df.dropna(subset=["oja_id", "occupation4d", "last_active_date", "skill"], inplace=True)

# 2. Πρόσθεσε στήλη τριμήνου
df["last_active_date"] = pd.to_datetime(df["last_active_date"])
df["quarter"] = df["last_active_date"].dt.to_period("Q")

# 3. Βρόχος ανά τρίμηνο
output_dir = "data/temporal_edges_per_quarter"
os.makedirs(output_dir, exist_ok=True)

for quarter, group in tqdm(df.groupby("quarter")):
    G = nx.DiGraph()
    
    # Ομαδοποίηση ανά αγγελία
    for oja_id, post_group in group.groupby("oja_id"):
        skills = list(post_group.sort_values("last_active_date")["skill"])
        # Κατασκευή κατευθυνόμενων ακμών: skill[i] -> skill[i+1]
        for i in range(len(skills) - 1):
            src = skills[i]
            tgt = skills[i+1]
            if src != tgt:
                if G.has_edge(src, tgt):
                    G[src][tgt]["weight"] += 1
                else:
                    G.add_edge(src, tgt, weight=1)
    
    # Αποθήκευση ακμών
    edge_list = [{"source": u, "target": v, "weight": d["weight"]} for u, v, d in G.edges(data=True)]
    edge_df = pd.DataFrame(edge_list)
    edge_df.to_csv(f"{output_dir}/temporal_edges_{str(quarter)}.csv", index=False)

