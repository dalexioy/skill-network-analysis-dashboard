console.log("Dashboard.js loaded! window.top10Trends:", window.top10Trends);

document.addEventListener("DOMContentLoaded", function () {
    const metricSelect = document.getElementById("metricSelect");
    const communitySelect = document.getElementById("communitySelect");

    if (metricSelect) {
        metricSelect.addEventListener("change", plotTop10Trends);
        plotTop10Trends();
    }

    if (communitySelect) {
        communitySelect.addEventListener("change", () => {
            plotCommunityMetrics();
            plotSkillPath();
        });
        plotCommunityMetrics();
        plotSkillPath();
    }

    function plotTop10Trends() {
        const metric = metricSelect.value;
        const skills = [...new Set(window.top10Trends.map(d => d.skill))];
        const quarters = ["2024Q1", "2024Q2", "2024Q3", "2024Q4"];
        const traces = skills.map(skill => {
            const data = window.top10Trends.filter(d => d.skill === skill);
            return {
                x: quarters,
                y: quarters.map(q => {
                    const d = data.find(d => d.quarter === q);
                    return d ? d[metric] : null;
                }),
                name: skill,
                type: 'scatter',
                mode: 'lines+markers'
            };
        });
        Plotly.newPlot("top10TrendsChart", traces, {
            title: `Εξέλιξη Top-10 Skills (${metric.charAt(0).toUpperCase() + metric.slice(1)})`,
            yaxis: { title: metric.charAt(0).toUpperCase() + metric.slice(1) },
            xaxis: { title: "Quarter" }
        });
    }

    function plotCommunityMetrics() {
        const selectedLabel = communitySelect.value;
        const data = window.metricsData.filter(d => d.label === selectedLabel);
        const quarters = [...new Set(data.map(d => d.quarter))].sort();

        const traces1 = ["n_skills", "avg_degree"].map(metric => ({
            x: quarters,
            y: quarters.map(q => {
                const row = data.find(d => d.quarter === q);
                return row ? parseFloat(row[metric]) : null;
            }),
            name: metric,
            type: 'scatter',
            mode: 'lines+markers'
        }));

        Plotly.newPlot("communityChart1", traces1, {
            title: `Nodes & Avg Degree για ${selectedLabel}`,
            yaxis: { title: "Τιμή" },
            xaxis: { title: "Quarter" }
        });

        const traces2 = ["avg_pagerank", "avg_betweenness", "density"].map(metric => ({
            x: quarters,
            y: quarters.map(q => {
                const row = data.find(d => d.quarter === q);
                return row ? parseFloat(row[metric]) : null;
            }),
            name: metric,
            type: 'scatter',
            mode: 'lines+markers'
        }));

        Plotly.newPlot("communityChart2", traces2, {
            title: `Centrality Metrics για ${selectedLabel}`,
            yaxis: { title: "Τιμή Μετρικής" },
            xaxis: { title: "Quarter" }
        });
    }

    function plotSkillPath() {
        const selectedLabel = communitySelect.value;
        const row = window.skillPaths.find(d => d.group === selectedLabel);
        if (!row) return;

        const nodes = row.path.split(" → ").map(s => s.trim());

        const x = nodes.map((_, i) => i);
        const y = nodes.map(_ => 0); // οριζόντια τοποθέτηση

        // Κόμβοι
        const node_trace = {
            x: x,
            y: y,
            mode: 'markers+text',
            type: 'scatter',
            marker: { size: 40, color: '#4682B4' },
            text: nodes,
            textposition: 'bottom center',
            hoverinfo: 'text',
            showlegend: false
        };

        // Συνδέσεις
        const edge_traces = nodes.slice(0, -1).map((source, i) => ({
            type: 'scatter',
            mode: 'lines',
            x: [x[i], x[i + 1]],
            y: [y[i], y[i + 1]],
            line: {
                color: '#888',
                width: 2
            },
            hoverinfo: 'none',
            showlegend: false
        }));

        const layout = {
            title: `🧭 Κορυφαίο Skill Path για: ${selectedLabel}`,
            margin: { l: 20, r: 20, t: 50, b: 20 },
            xaxis: { visible: false },
            yaxis: { visible: false },
            height: 250
        };

        Plotly.newPlot("skillPathChart", [node_trace, ...edge_traces], layout);
    }
});
