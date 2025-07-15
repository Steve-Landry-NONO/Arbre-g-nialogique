// fichier : script.js

d3.json("data.json").then(function(data) {
  const width = 960;
  const dx = 10;
  const dy = width / 6;

  const tree = d3.tree().nodeSize([dx, dy]);
  const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

  // Transformation récursive pour injecter les spouses comme enfants secondaires
  function transformerStructure(node) {
    if (node.spouses && node.spouses.length > 0) {
      node.children = node.spouses.map(spouse => {
        let s = {
          name: spouse.name + " (époux(se))",
          date: spouse.date,
          profession: spouse.profession,
          children: spouse.children ? spouse.children.map(transformerStructure) : []
        };
        return s;
      });
    }
    return node;
  }

  const root = d3.hierarchy(transformerStructure(data));
  root.x0 = dy / 2;
  root.y0 = 0;

  const svg = d3.select("#tree-container").append("svg")
      .attr("viewBox", [-dy / 3, -dx, width, dx * 20])
      .style("font", "14px sans-serif")
      .style("user-select", "none");

  const gLink = svg.append("g")
      .attr("fill", "none")
      .attr("stroke", "#555")
      .attr("stroke-opacity", 0.4)
      .attr("stroke-width", 1.5);

  const gNode = svg.append("g")
      .attr("cursor", "pointer")
      .attr("pointer-events", "all");

  function update(source) {
    const nodes = root.descendants().reverse();
    const links = root.links();

    tree(root);

    let left = root;
    let right = root;
    root.eachBefore(node => {
      if (node.x < left.x) left = node;
      if (node.x > right.x) right = node;
    });

    const height = right.x - left.x + dx * 2;

    const transition = svg.transition().duration(750)
        .attr("viewBox", [-dy / 3, left.x - dx, width, height]);

    const node = gNode.selectAll("g")
        .data(nodes, d => d.data.name + d.depth);

    const nodeEnter = node.enter().append("g")
        .attr("transform", d => `translate(${source.y0},${source.x0})`)
        .on("click", (event, d) => {
          d.children = d.children ? null : d._children;
          update(d);
        });

    nodeEnter.append("circle")
        .attr("r", 4.5)
        .attr("fill", d => d._children ? "#555" : "#999");

    nodeEnter.append("title")
        .text(d => `Nom : ${d.data.name}\nNaissance : ${d.data.date || 'Inconnue'}\nProfession : ${d.data.profession || 'Non renseignée'}`);

    nodeEnter.append("text")
        .attr("dy", "0.31em")
        .attr("x", d => d._children ? -10 : 10)
        .attr("text-anchor", d => d._children ? "end" : "start")
        .text(d => d.data.name)
        .clone(true).lower()
        .attr("stroke", "white");

    const nodeUpdate = node.merge(nodeEnter).transition(transition)
        .attr("transform", d => `translate(${d.y},${d.x})`);

    nodeUpdate.select("circle")
        .attr("fill", d => d._children ? "#555" : "#999");

    const nodeExit = node.exit().transition(transition).remove()
        .attr("transform", d => `translate(${source.y},${source.x})`);

    nodeExit.select("circle").attr("r", 1e-6);
    nodeExit.select("text").style("fill-opacity", 1e-6);

    const link = gLink.selectAll("path")
        .data(links, d => d.target.data.name + d.target.depth);

    const linkEnter = link.enter().append("path")
        .attr("d", d => {
          const o = {x: source.x0, y: source.y0};
          return diagonal({source: o, target: o});
        });

    link.merge(linkEnter).transition(transition)
        .attr("d", diagonal);

    link.exit().transition(transition).remove()
        .attr("d", d => {
          const o = {x: source.x, y: source.y};
          return diagonal({source: o, target: o});
        });

    root.eachBefore(d => {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  }

  root.children?.forEach(child => {
    child._children = child.children;
    child.children = null;
  });

  update(root);
});
