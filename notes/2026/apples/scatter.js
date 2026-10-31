
const csvFile = "apples.csv";
const container = "#scatter-plot";

// Plot settings
const margin = { top: 20, right: 25, bottom: 55, left: 65 };
const pointRadius = 4;

// Load CSV and convert coordinates to numbers
d3.csv(csvFile, d => ({
  name: d.name,
  x: +d.sugar,
  y: +d.acid,
  size: +d.yield
})).then(data => {
  data = data.filter(d =>
    Number.isFinite(d.x) && Number.isFinite(d.y)
  );

  const element = d3.select(container).node();
  const width = element.clientWidth;
  const height = 500;

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // SVG canvas
  const svg = d3.select(container)
    .append("svg")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("width", "100%")
    .attr("height", "auto");

  const plot = svg.append("g")
    .attr("transform",
      `translate(${margin.left},${margin.top})`
    );

  // Scales, with a little padding around the data
  const x = d3.scaleLinear()
    .domain(d3.extent(data, d => d.x))
    .nice()
    .range([0, innerWidth]);

  const y = d3.scaleLinear()
    .domain(d3.extent(data, d => d.y))
    .nice()
    .range([innerHeight, 0]);

const r = d3.scaleSqrt()
  .domain(d3.extent(data, d => d.size))
  .range([2, 12]);

  // Axes
  plot.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x))
    .call(g => g.select(".domain").attr("stroke", "#888"))
    .call(g => g.selectAll(".tick line").attr("stroke", "#ddd"));

  plot.append("g")
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").attr("stroke", "#888"))
    .call(g => g.selectAll(".tick line").attr("stroke", "#ddd"));

  // Axis labels
  plot.append("text")
    .attr("class", "axis-label")
    .attr("x", innerWidth / 2)
    .attr("y", innerHeight + 45)
    .attr("text-anchor", "middle")
    .text("sugar");

  plot.append("text")
    .attr("class", "axis-label")
    .attr("transform", "rotate(-90)")
    .attr("x", -innerHeight / 2)
    .attr("y", -45)
    .attr("text-anchor", "middle")
    .text("acid");

  // Tooltip
  const tooltip = d3.select(container)
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

  // Data points
  plot.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => x(d.x))
    .attr("cy", d => y(d.y))
    .attr("r", d => r(d.size))
    .attr("class", "point")
  .on("mouseover", function(event, d) {
    d3.select(this)
      .attr("r", r(d.size) * 1.5)
      .attr("fill", "#000");

    tooltip
      .style("opacity", 1)
      .text(d.name);
  })
  .on("mouseout", function(event, d) {
    d3.select(this)
      .attr("r", r(d.size))
      .attr("fill", "#777");

    tooltip.style("opacity", 0);
  })
    .on("mousemove", function(event) {
      const [mx, my] = d3.pointer(event, element);

      tooltip
        .style("left", `${mx + 12}px`)
        .style("top", `${my + 12}px`);
    })

}).catch(error => {
  console.error("Could not load CSV:", error);
});