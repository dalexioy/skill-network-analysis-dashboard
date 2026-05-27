import json
import pandas as pd
from django.shortcuts import render

def index_view(request):
    # Βασικά στατιστικά
    num_jobs = "1.200.000"
    num_unique_skills = 1086

    # === Top-10 Skills Trends ===
    with open("data/top10_skills_quarterly_centralities.json", "r", encoding="utf-8") as f:
        top10_trends = json.load(f)
    available_metrics = ["pagerank", "betweenness"]

    # === Skill Paths per Group ===
    paths_df = pd.read_csv("data/top_skill_paths_per_group.csv")
    paths_data = paths_df.to_dict(orient="records")

    # === Evolution Metrics ===
    metrics_file = "data/evolution_per_community/community_metrics_labeled.csv"
    metrics_df = pd.read_csv(metrics_file)
    metrics_df['top_skills'] = metrics_df['top_skills'].apply(
        lambda x: ', '.join(eval(x)) if isinstance(x, str) and x.startswith("[") else str(x)
    )
    unique_labels = sorted(metrics_df["label"].dropna().unique())

    # === Jaccard Matrix (flattened for HTML table) ===
    jaccard_df = pd.read_csv("data/jaccard_matrix_by_label1.csv", index_col=0)
    jaccard_columns = list(jaccard_df.columns)
    jaccard_flat = []
    for row_label in jaccard_df.index:
        entry = {"row_label": row_label}
        for col in jaccard_columns:
            entry[col] = round(jaccard_df.loc[row_label, col], 2)
        jaccard_flat.append(entry)

    # === Modularity Table ===
    temporal_mod = pd.read_csv("data/temporal_modularity_by_label.csv")
    contemp_mod = pd.read_csv("data/contemporaneous_modularity_by_label.csv")
    temporal_mod["type"] = "Temporal"
    contemp_mod["type"] = "Contemporaneous"
    combined_mod = pd.concat([temporal_mod, contemp_mod], ignore_index=True)
    modularity_table = combined_mod.pivot(index="quarter", columns="type", values="modularity_by_label").round(3)

    # === Context ===
    context = {
        "num_jobs": num_jobs,
        "num_unique_skills": num_unique_skills,
        "top10_trends": top10_trends,
        "available_metrics": available_metrics,
        "metrics_data": metrics_df.to_dict(orient="records"),
        "evolution_data": metrics_df.to_dict(orient="records"),
        "community_labels": unique_labels,
        "skill_paths": paths_data,
        "jaccard_matrix": jaccard_flat,
        "jaccard_columns": jaccard_columns,
        "modularity_table": modularity_table.reset_index().to_dict(orient="records")
    }

    return render(request, "dashboard.html", context)
