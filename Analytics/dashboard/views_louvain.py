# dashboard/views_louvain.py
import json
from django.shortcuts import render

def louvain_network_tool(request):
    selected_quarter = request.GET.get("quarter", "2024Q1")
    file_path = f"data/quarterly_networks/{selected_quarter}_network.json"

    with open(file_path, "r") as f:
        network_data = json.load(f)

    return render(request, "louvain_network_tool.html", {
        "network_data": json.dumps(network_data),
        "selected_quarter": selected_quarter
    })
