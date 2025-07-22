// fichier : script.js

// Visualisation de l’arbre généalogique avec nœuds de mariage explicites

const width = 960;
const height = 600;

const svg = d3.select("#tree-container")
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", "translate(40,40)");

// Échelle de couleur pour genre
const color = d => {
  if (d.type === "mariage") return "#999";
  return d.sexe === "H" ? "#3498db" : "#e74c3c";
};

// Taille des nœuds
const radius = d => d.type === "mariage" ? 5 : 12;

// Charger les données
fetch("data.json")
  .then(response => response.json())
  .then(data => {
    const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id).distance(80))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    // Lignes de liens
    const link = svg.append("g")
      .attr("stroke", "#ccc")
      .attr("stroke-width", 1.5)
      .selectAll("line")
      .data(data.links)
      .enter().append("line");

    // Nœuds
    const node = svg.append("g")
      .selectAll("circle")
      .data(data.nodes)
      .enter().append("circle")
      .attr("r", d => radius(d))
      .attr("fill", d => color(d))
      .call(drag(simulation));

    // Étiquettes
    const label = svg.append("g")
      .selectAll("text")
      .data(data.nodes.filter(d => d.type === "personne"))
      .enter().append("text")
      .text(d => d.name)
      .attr("font-size", 12)
      .attr("dy", -15)
      .attr("text-anchor", "middle");

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });
  });

function drag(simulation) {
  return d3.drag()
    .on("start", function (event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    })
    .on("drag", function (event, d) {
      d.fx = event.x;
      d.fy = event.y;
    })
    .on("end", function (event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    });
}
