import pandas as pd
import matplotlib.pyplot as plt
import os

# 🔄 Φόρτωση CSV
df = pd.read_csv("data/results/pagerank_top30_skills_contemporaneous.csv")

# ✅ Αντικατέστησε αν η στήλη ονομάζεται "community_label" αντί για "group"
df = df.rename(columns={"community_label": "group"})

# 🔃 Ταξινόμηση τριμήνων για σωστή σειρά
quarter_order = ["2024Q1", "2024Q2", "2024Q3", "2024Q4"]
df["quarter"] = pd.Categorical(df["quarter"], categories=quarter_order, ordered=True)

# 📂 Δημιουργία φακέλου αποθήκευσης (αν δεν υπάρχει)
os.makedirs("data/plots", exist_ok=True)

# 📈 Δημιουργία γραφήματος ανά ομάδα
for group in df["group"].dropna().unique():
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

    # 🔘 Αποθήκευση γραφήματος
    filename = group.replace(" ", "_").replace("&", "and").replace(",", "").replace("__", "_")
    plt.savefig(f"data/plots/pagerank_top5_{filename}.png", dpi=300)
    plt.close()

print("✅ Ολοκληρώθηκε: Δημιουργήθηκαν όλα τα γραφήματα Pagerank ανά θεματική κοινότητα.")