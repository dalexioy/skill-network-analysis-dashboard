# analyze_top_skills_over_time.py
import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# Δημιουργία φακέλου αν δεν υπάρχει
os.makedirs("data/plots", exist_ok=True)

# 🔁 Βήμα 1: Paths & Φόρτωση Δεδομένων
quarters = ["2024Q1", "2024Q2", "2024Q3", "2024Q4"]
enriched_paths = {q: f"data/quarterly_louvain_results/enriched_louvain_{q}.json" for q in quarters}

# Φόρτωση global top-10 skills ανά κοινότητα
with open("outputs/top10_skills_per_global_community.json", "r", encoding="utf-8") as f:
    global_data = json.load(f)

# Επιλογή top-5 ανά κοινότητα
selected_skills = []
skill_to_group = {}
for group, skills in global_data.items():
    for s in skills[:5]:
        skill = s["skill"]
        selected_skills.append(skill)
        skill_to_group[skill] = group

# 🔁 Συγκέντρωση των μετρικών
records = []
for quarter, path in enriched_paths.items():
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        skill = entry["skill"]
        if skill in selected_skills:
            records.append({
                "skill": skill,
                "quarter": quarter,
                "community_label": entry.get("community_label", "Unknown"),
                "pagerank": entry.get("pagerank"),
                "betweenness": entry.get("betweenness"),
                "degree": entry.get("degree_centrality"),
                "group": skill_to_group.get(skill)
            })

df = pd.DataFrame(records)

# 📈 Plot ανά group: Pagerank εξέλιξη top-5 skills
for group in df["group"].unique():
    plt.figure(figsize=(10, 5))
    group_df = df[df["group"] == group]
    for skill in group_df["skill"].unique():
        temp = group_df[group_df["skill"] == skill].sort_values("quarter")
        plt.plot(temp["quarter"], temp["pagerank"], label=skill, marker="o")
    plt.title(f"Pagerank Evolution – {group}")
    plt.xlabel("Quarter")
    plt.ylabel("Pagerank")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"data/plots/pagerank_top5_{group.replace(' ', '_')}.png")
    plt.close()

# 🔁 Πίνακας: μεταβολή label ανά skill
label_changes = defaultdict(dict)
for _, row in df.iterrows():
    label_changes[row["skill"]][row["quarter"]] = row["community_label"]

label_change_df = pd.DataFrame(label_changes).T
label_change_df.to_csv("data/plots/skill_label_changes.csv")

# 📊 Plot: Μέση τιμή Pagerank ανά κοινότητα
plt.figure(figsize=(12, 6))
for group in df["group"].unique():
    group_df = df[df["group"] == group]
    grouped = group_df.groupby("quarter")["pagerank"].mean()
    plt.plot(grouped.index, grouped.values, label=group, marker="o")
plt.title("Average Pagerank per Community Group")
plt.xlabel("Quarter")
plt.ylabel("Mean Pagerank")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("data/plots/pagerank_mean_per_group.png")
plt.close()
