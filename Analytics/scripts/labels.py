import json

# Ορισμός labels βάσει community ID (για temporal Louvain)
temporal_labels = {
    0: "Project & Analytical Thinking",
    1: "ICT Hardware & Automation Tools",
    2: "Soft Skills & Teamwork Competencies",
    3: "Digital Office Tools & Leadership Skills",
    4: "Software Engineering & Programming",
    5: "Customer Support, Responsibility & Quality"
}

# 📁 Αρχεία εισόδου/εξόδου
input_file = "data/temporal_enriched.json"
output_file = "data/temporal_louvain_labeled.json"

# 🔹 Φόρτωση JSON
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 🔹 Ενσωμάτωση ετικέτας σε κάθε εγγραφή
for entry in data:
    comm_id = entry.get("community")
    entry["community_label"] = temporal_labels.get(comm_id, f"Community {comm_id}")

# 💾 Αποθήκευση εμπλουτισμένου αρχείου
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Αποθηκεύτηκε: {output_file}")
