import json
import pandas as pd
from collections import defaultdict

# 🔹 1. Φόρτωση αρχείων
with open("data/temporal.json", "r", encoding="utf-8") as f:
    global_data = json.load(f)

with open("data/quarterly_louvain_results/all_quarters_nodes.json", "r", encoding="utf-8") as f:
    temporal_data = json.load(f)

# 🔹 2. Δημιουργία mappings
# skill → global community
global_comm_map = {entry["skill"]: entry["community"] for entry in global_data}

# 🔹 3. Ομαδοποίηση skills σε temporal communities
temporal_groups = defaultdict(lambda: defaultdict(set))  # quarter → temporal_comm → set(skills)
for entry in temporal_data:
    temporal_groups[entry["quarter"]][entry["community"]].add(entry["skill"])

# 🔹 4. Ομαδοποίηση skills σε global communities
global_groups = defaultdict(set)  # global_comm → set(skills)
for entry in global_data:
    global_groups[entry["community"]].add(entry["skill"])

# 🔹 5. Υπολογισμός Jaccard Similarity: temporal vs global ανά τρίμηνο
results = []

for quarter in temporal_groups:
    for temp_comm, temp_skills in temporal_groups[quarter].items():
        for global_comm, global_skills in global_groups.items():
            intersection = temp_skills & global_skills
            union = temp_skills | global_skills
            jaccard = round(len(intersection) / len(union), 4) if union else 0
            results.append({
                "quarter": quarter,
                "temporal_comm": temp_comm,
                "global_comm": global_comm,
                "jaccard": jaccard,
                "intersection_size": len(intersection),
                "union_size": len(union)
            })

# 🔹 6. Αποθήκευση σε αρχείο
df_jaccard = pd.DataFrame(results)
df_jaccard.sort_values(by=["quarter", "temporal_comm", "jaccard"], ascending=[True, True, False], inplace=True)
df_jaccard.to_csv("data/jaccard_temporal_vs_global.csv", index=False, encoding="utf-8")

print("✅ Αποθηκεύτηκε: data/jaccard_temporal_vs_global.csv")
