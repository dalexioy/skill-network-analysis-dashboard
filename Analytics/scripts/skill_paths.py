import pandas as pd
import json
from itertools import permutations
from collections import defaultdict

# === Βήμα 1: Φόρτωση αρχείου temporal.json ===
with open("data/temporal.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# === Βήμα 2: Ομαδοποίηση skills ανά community label ===
group_to_skills = defaultdict(list)

for entry in data:
    skill = entry["skill"]
    group = entry["community_label"]
    pagerank = entry["pagerank"]
    group_to_skills[group].append((skill, pagerank))

# === Βήμα 3: Για κάθε group βρίσκουμε όλα τα paths ABCDE και κρατάμε τα 2 κορυφαία ===
top_paths_per_group = []

for group, skill_pagerank_list in group_to_skills.items():
    # Κρατάμε τα top 7 skills για ασφάλεια (αν κάποιο έχει ίδιο pagerank)
    sorted_skills = sorted(skill_pagerank_list, key=lambda x: x[1], reverse=True)[:7]
    skill_names = [s[0] for s in sorted_skills]

    # Όλα τα δυνατά paths ABCDE (χωρίς επανάληψη)
    all_paths = list(permutations(skill_names, 6))

    path_scores = []
    for path in all_paths:
        mean_pagerank = sum(dict(sorted_skills)[skill] for skill in path) / len(path)
        path_scores.append((path, mean_pagerank))

    # Ταξινόμηση και επιλογή top 2 paths
    top_paths = sorted(path_scores, key=lambda x: x[1], reverse=True)[:2]

    for path, score in top_paths:
        top_paths_per_group.append({
            "group": group,
            "path": " → ".join(path),
            "mean_pagerank": round(score, 6)
        })

# === Βήμα 4: Αποθήκευση σε CSV και εμφάνιση ===
df_paths = pd.DataFrame(top_paths_per_group)
df_paths = df_paths.sort_values(["group", "mean_pagerank"], ascending=[True, False])
df_paths.to_csv("data/top_2_skill_paths_per_group.csv", index=False)

print("✅ Αποθηκεύτηκαν τα top skill paths ανά group στο:")
print("➡️ data/top_2_skill_paths_per_group.csv")
print(df_paths.head(10))
