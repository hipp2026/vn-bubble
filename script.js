const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("#chart")
  .attr("viewBox", [0, 0, width, height]);

const size = d3.scaleSqrt()
  .domain([0, 5_000_000])
  .range([35, 100]);

const color = d3.scaleLinear()
  .domain([-5, 0, 5])
  .range(["#ff4d4d", "#666", "#4dff88"]);

fetch("data.json")
  .then(res => res.json())
  .then(raw => {

    const data = Object.entries(raw).map(([symbol, v]) => ({
      symbol,
      change: v.change_pct,
      volume: v.volume
    }));

    const sim = d3.forceSimulation(data)
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision",
        d3.forceCollide().radius(d => size(d.volume) + 2)
      )
      .on("tick", () => {
        node.attr("transform", d => `translate(${d.x},${d.y})`);
      });

    const node = svg.selectAll("g")
      .data(data)
      .enter()
      .append("g");

    node.append("circle")
      .attr("r", d => size(d.volume))
      .attr("fill", d => color(d.change))
      .attr("opacity", 0.9);

    node.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "-0.2em")
      .attr("fill", "white")
      .style("font-weight", "bold")
      .text(d => d.symbol);

    node.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "1.1em")
      .attr("fill", "white")
      .style("font-size", "12px")
      .text(d => `${d.change.toFixed(2)}%`);

  });