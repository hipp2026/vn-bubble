const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("#chart")
  .attr("viewBox", [0, 0, width, height]);

const size = d3.scaleSqrt()
  .domain([0, 1e9])      // volume hoặc market cap
  .range([40, 100]);

const color = d3.scaleLinear()
  .domain([-5, 0, 5])
  .range(["red", "#555", "green"]);

// 🔴 LOAD DATA THẬT
fetch("data.json")
  .then(res => res.json())
  .then(raw => {

    // chuyển JSON → mảng cho D3
    const data = Object.entries(raw).map(([symbol, v]) => ({
      symbol: symbol,
      change: v.change_pct,
      cap: v.volume     // dùng volume làm kích thước bubble
    }));

    const sim = d3.forceSimulation(data)
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision",
        d3.forceCollide().radius(d => size(d.cap) + 2)
      )
      .on("tick", () => {
        node.attr("transform", d => `translate(${d.x},${d.y})`);
      });

    const node = svg.selectAll("g")
      .data(data)
      .enter()
      .append("g");

    node.append("circle")
      .attr("r", d => size(d.cap))
      .attr("fill", d => color(d.change))
      .attr("opacity", 0.85);

    node.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .attr("fill", "white")
      .style("font-weight", "bold")
      .text(d => d.symbol);

  });