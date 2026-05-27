import pandas as pd
import json
import os
from collections import defaultdict

# 📥 Φόρτωση global communities με labels
with open("data/contemporaneous.json", "r", encoding="utf-8") as f:
    global_data = json.load(f)

# Δημιουργία: community_id → skill set και label
global_comm_to_skills = defaultdict(set)
global_comm_to_label = {}

for entry in global_data:
    comm_id = entry["community"]
    skill = entry["skill"]
    global_comm_to_skills[comm_id].add(skill)
    global_comm_to_label[comm_id] = entry["community_label"]

# 📥 Φόρτωση όλων των κόμβων όλων των τριμήνων
with open("contemporaneous_louvain_results/all_quarter_nodes.json", "r", encoding="utf-8") as f:
    quarter_data = json.load(f)

# Ομαδοποίηση ανά (quarter, community_id)
quarter_comm_to_skills = defaultdict(set)

for entry in quarter_data:
    key = (entry["quarter"], entry["community"])
    quarter_comm_to_skills[key].add(entry["skill"])

# Υπολογισμός Jaccard και αντιστοίχιση label
results = []

for (quarter, comm_id), skill_set in quarter_comm_to_skills.items():
    best_score = 0
    best_match_id = None
    best_label = "Unmatched"

    for g_id, g_skills in global_comm_to_skills.items():
        intersection = skill_set & g_skills
        union = skill_set | g_skills
        if not union:
            continue
        jaccard = len(intersection) / len(union)
        if jaccard > best_score:
            best_score = jaccard
            best_match_id = g_id

    if best_score >= 0.1:
        best_label = global_comm_to_label.get(best_match_id, "Unmatched")

    results.append({
        "quarter": quarter,
        "community_id": comm_id,
        "assigned_label": best_label,
        "matched_global_id": best_match_id if best_score >= 0.1 else None,
        "jaccard_similarity": round(best_score, 4)
    })

# 💾 Αποθήκευση
df = pd.DataFrame(results)
os.makedirs("data/results", exist_ok=True)
df.to_csv("data/results/quarterly_communities_assigned_labels.csv", index=False)

print("✅ Ολοκληρώθηκε: data/results/quarterly_communities_assigned_labels.csv")
