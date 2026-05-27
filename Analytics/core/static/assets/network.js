document.addEventListener("DOMContentLoaded", function () {
  const metricSelect = document.getElementById("metricSelect");
  const thresholdSlider = document.getElementById("thresholdSlider");
  const thresholdValue = document.getElementById("thresholdValue");

  const SELECTED_SKILLS = new Set([
    "work in teams", "adapt to change", "teamwork principles", "team building", "English",
    "customer service", "assist customers", "assume responsibility", "follow company standards", "manage quality",
    "have computer literacy", "use microsoft office", "business ICT systems", "office software", "think creatively",
    "hardware components", "use ICT hardware", "computer technology", "use content management system software", "web analytics",
    "project management", "create solutions to problems", "use office systems", "computer science", "database",
    "computer programming", "use object-oriented programming", "Java (computer programming)", "SQL", "ICT system programming"
  ]);

  // Create dropdown για κοινότητα
  const communitySelect = document.createElement("select");
  communitySelect.id = "communitySelect";
  communitySelect.className = "form-select mt-2 mb-2";
  communitySelect.innerHTML = `<option value="all">Όλες οι κοινότητες</option>`;
  document.querySelector(".container").prepend(communitySelect);

  // Create edge weight slider
  const edgeWeightSlider = document.createElement("input");
  edgeWeightSlider.type = "range";
  edgeWeightSlider.min = 50;
  edgeWeightSlider.max = 3000;
  edgeWeightSlider.step = 100;
  edgeWeightSlider.value = 200;
  edgeWeightSlider.id = "edgeWeightSlider";
  edgeWeightSlider.className = "form-range";

  const edgeWeightLabel = document.createElement("label");
  edgeWeightLabel.innerHTML = `Min Edge Weight: <span id='edgeWeightValue'>200</span>`;

  const edgeWeightWrapper = document.createElement("div");
  edgeWeightWrapper.className = "mt-2 mb-3";
  edgeWeightWrapper.appendChild(edgeWeightLabel);
  edgeWeightWrapper.appendChild(edgeWeightSlider);
  document.querySelector(".container").prepend(edgeWeightWrapper);

  edgeWeightSlider.addEventListener("input", function () {
    document.getElementById("edgeWeightValue").innerText = edgeWeightSlider.value;
    drawGraph();
  });

  function drawGraph() {
    const metric = metricSelect.value;
    const threshold = parseFloat(thresholdSlider.value);
    const selectedCommunity = communitySelect.value;
    const minEdgeWeight = parseInt(edgeWeightSlider.value);
    thresholdValue.innerText = threshold;

    const filteredNodes = NETWORK_DATA.nodes.filter(n =>
      SELECTED_SKILLS.has(n.id) &&
      parseFloat(n[metric]) >= threshold &&
      (selectedCommunity === "all" || n.community.toString() === selectedCommunity)
    );

    const nodeIds = new Set(filteredNodes.map(n => n.id));
    const filteredEdges = NETWORK_DATA.edges.filter(e =>
      nodeIds.has(e.source) && nodeIds.has(e.target) && e.weight >= minEdgeWeight
    );

    const nodeIndex = {};
    filteredNodes.forEach((n, i) => nodeIndex[n.id] = i);

    const x = [], y = [], text = [], colors = [], sizes = [], hover = [];
    filteredNodes.forEach((node, i) => {
      x.push(Math.cos(i * 2 * Math.PI / filteredNodes.length));
      y.push(Math.sin(i * 2 * Math.PI / filteredNodes.length));
      text.push(node.id);
      hover.push(`${node.community_label}<br>${metric}: ${node[metric].toFixed(4)}`);
      colors.push(node.community);
      sizes.push(10 + node[metric] * 100);
    });

    const nodeTrace = {
      x: x,
      y: y,
      text: text,
      mode: 'markers+text',
      textposition: 'top center',
      hovertext: hover,
      marker: {
        size: sizes,
        color: colors,
        colorscale: 'Viridis',
        showscale: false
      },
      type: 'scatter'
    };

    const edgeTraces = filteredEdges.map(e => {
      const src = nodeIndex[e.source];
      const tgt = nodeIndex[e.target];
      if (src === undefined || tgt === undefined) return null;
      return {
        x: [x[src], x[tgt], null],
        y: [y[src], y[tgt], null],
        mode: 'lines',
        line: { width: 1, color: '#bbb' },
        type: 'scatter',
        hoverinfo: 'none'
      };
    }).filter(Boolean);

    const data = [...edgeTraces, nodeTrace];

    const layout = {
      title: "Louvain Network – 30 επιλεγμένα skills",
      showlegend: false,
      hovermode: 'closest',
      margin: { t: 50, l: 20, r: 20, b: 20 },
      xaxis: { visible: false },
      yaxis: { visible: false }
    };

    Plotly.newPlot("networkGraph", data, layout, { responsive: true });

    // Update δυναμικό legend
    createLegend(filteredNodes);
  }

  // Δυναμική δημιουργία επιλογών κοινότητας
  const uniqueCommunities = [...new Map(
    NETWORK_DATA.nodes
      .filter(n => SELECTED_SKILLS.has(n.id))
      .map(n => [n.community.toString(), n.community_label])
  ).entries()].sort((a, b) => a[1].localeCompare(b[1]));

  uniqueCommunities.forEach(([id, label]) => {
    const opt = document.createElement("option");
    opt.value = id;
    opt.text = `${label}`;
    communitySelect.appendChild(opt);
  });

  // Δυναμικό legend δημιουργία (αφαιρεί το static)
  function createLegend(nodes) {
    const legendContainer = document.querySelector("#dynamicLegend");
    if (!legendContainer) return;

    legendContainer.innerHTML = "";  // Καθαρισμός

    const uniqueGroups = [...new Set(nodes.map(n => n.community_label))];

    uniqueGroups.forEach((label, i) => {
      const colorBox = document.createElement("span");
      colorBox.style = `
        display:inline-block;
        width:18px;
        height:18px;
        background-color:rgba(0, 150, 255, ${0.3 + (i / uniqueGroups.length)});
        margin-right:8px;
        border-radius:4px;
      `;
      const item = document.createElement("li");
      item.appendChild(colorBox);
      item.appendChild(document.createTextNode(label));
      legendContainer.appendChild(item);
    });
  }

  // Event listeners
  metricSelect.addEventListener("change", drawGraph);
  thresholdSlider.addEventListener("input", drawGraph);
  communitySelect.addEventListener("change", drawGraph);

  drawGraph();
});
