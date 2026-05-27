import json
import pandas as pd

# 📁 Αρχείο εισόδου
input_json = "data/temporal_enriched.json"
output_csv = "data/top10_skills_per_community.csv"

# 🔹 Φόρτωση JSON
with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# 🔹 Μετατροπή σε DataFrame
df = pd.DataFrame(data)

# 🔹 Top-10 skills ανά community με βάση Pagerank
top_skills_df = (
    df.sort_values(by=["community", "pagerank"], ascending=[True, False])
    .groupby("community")
    .head(10)
    .reset_index(drop=True)
)

# 🔹 Επιλογή πεδίων
top_skills_df = top_skills_df[
    ["community", "skill", "pagerank", "skill_hier1", "skill_hier2", "skill_hier3"]
]

# 💾 Αποθήκευση σε CSV
top_skills_df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"✅ Αποθηκεύτηκε το αρχείο: {output_csv}")
