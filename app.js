const data = [
  { symbol: "VCB", change: 1.8, cap: 400 },
  { symbol: "FPT", change: 2.5, cap: 300 },
  { symbol: "HPG", change: -1.2, cap: 250 }
];

const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("#chart")
  .attr("viewBox", [0, 0, width, height]);

const size = d3.scaleSqrt()
  .domain([0, 400])
  .range([40, 90]);

const color = d3.scaleLinear()
  .domain([-5, 0, 5])
  .range(["red", "gray", "green"]);

const sim = d3.forceSimulation(data)
  .force("center", d3.forceCenter(width/2, height/2))
  .force("collision", d3.forceCollide().radius(d => size(d.cap)))
  .on("tick", () => {
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  });

const node = svg.selectAll("g")
  .data(data)
  .enter()
  .append("g");

node.append("circle")
  .attr("r", d => size(d.cap))
  .attr("fill", d => color(d.change));

node.append("text")
  .attr("text-anchor", "middle")
  .attr("dy", ".35em")
  .attr("fill", "white")
  .text(d => d.symbol);
