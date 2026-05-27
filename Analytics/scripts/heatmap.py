import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# 🔄 Φόρτωση CSV
df = pd.read_csv("data/plots/pagerank_and_community_top30_contemporaneous.csv")

# ✅ Κανονικοποίηση των labels (strip whitespace, lower if θέλεις)
df["community_label"] = df["community_label"].apply(lambda x: str(x).strip() if pd.notnull(x) else x)

# 📊 Pivot: skills ως γραμμές, quarters ως στήλες, values = community label
pivot_df = df.pivot(index="skill", columns="quarter", values="community_label")

# 🔢 Μετατροπή labels σε integers για heatmap
labels = sorted(set(str(x).strip() for x in pivot_df.values.ravel() if pd.notnull(x)))
label_to_int = {label: i for i, label in enumerate(labels)}
int_to_label = {v: k for k, v in label_to_int.items()}
df_int = pivot_df.replace(label_to_int)

# 🎨 Παλέτα χρωμάτων
palette = sns.color_palette("tab20", len(label_to_int))
color_map = {label: palette[i] for i, label in enumerate(label_to_int)}

# 🖼️ Heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(df_int, cmap=palette, cbar=False, linewidths=0.5, linecolor='gray')

plt.title("Skill Community Label Changes Over Time ", fontsize=14)
plt.xlabel("Quarter")
plt.ylabel("Skill")
plt.xticks(rotation=45)

# ➕ Legend
legend_patches = [Patch(color=color_map[label], label=label) for label in label_to_int]
plt.legend(
    handles=legend_patches,
    bbox_to_anchor=(1.02, 1),
    loc='upper left',
    borderaxespad=0.,
    title="Community Labels"
)

plt.tight_layout()
plt.savefig("data/plots/skill_label_heatmap_contemporaneous.png", dpi=300)
plt.close()
