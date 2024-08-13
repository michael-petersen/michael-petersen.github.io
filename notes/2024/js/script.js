  // Calculate the value for a given (x, y)
  const value = (x, y) =>
    (1 + (x + y + 1) ** 2 * (19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2))
    * (30 + (2 * x - 3 * y) ** 2 * (18 - 32 * x + 12 * x * x + 48 * y - 36 * x * y + 27 * y ** 2));
  


const width = 500;
const height = 500;

    // You should have defined `x`, `y`, `xAxis`, `yAxis`, and `color` functions somewhere
  // They are required for this code to work
  x = d3.scaleLinear([-2, 2], [0, width + 28])
  y = d3.scaleLinear([-2, 1], [height, 0])



// Define the chart function
const chart = () => {

  
    // Create SVG element
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width + 28, height])
        .style("display", "block")
        .style("margin", "0 -14px")
        .style("width", "calc(100% + 28px)");
  
    // Append paths for contour lines
    svg.append("g")
        .attr("fill", "none")
        .attr("stroke", "#fff")
        .attr("stroke-opacity", 0.5)
      .selectAll("path")
      .data(contours)
      .join("path")
        .attr("fill", d => color(d.value))
        .attr("d", d3.geoPath());
  
    // Append x-axis
    svg.append("g")
        .call(xAxis);
  
    // Append y-axis
    svg.append("g")
        .call(yAxis);
  
    return svg.node();
  }
  
  // Define the grid function
  const grid = () => {
    const q = 4; // The level of detail, e.g., sample every 4 pixels in x and y.
    const x0 = -q / 2, x1 = width + 28 + q;
    const y0 = -q / 2, y1 = height + q;
    const n = Math.ceil((x1 - x0) / q);
    const m = Math.ceil((y1 - y0) / q);
    const grid = new Array(n * m);
    for (let j = 0; j < m; ++j) {
      for (let i = 0; i < n; ++i) {
        grid[j * n + i] = value(x.invert(i * q + x0), y.invert(j * q + y0));
      }
    }
    grid.x = -q;
    grid.y = -q;
    grid.k = q;
    grid.n = n;
    grid.m = m;
    return grid;
  }
  
  // Converts from grid coordinates (indexes) to screen coordinates (pixels).
  const transform = ({type, value, coordinates}) => {
    return {type, value, coordinates: coordinates.map(rings => {
      return rings.map(points => {
        return points.map(([x, y]) => ([
          grid.x + grid.k * x,
          grid.y + grid.k * y
        ]));
      });
    })};
  }
  
  const myGrid = grid();


console.log(grid.n);
console.log(grid.m);
thresholds =  d3.range(1, 20).map(n => 2 ** n)

  // Create contours
  const contours = d3.contours()
      .size([myGrid.n, myGrid.m])
      .thresholds(thresholds)
    (myGrid)
      .map(transform);
  

  
  xAxis = g => g
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisTop(x).ticks(width / height * 10))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick").filter(d => x.domain().includes(d)).remove())

  yAxis = g => g
    .attr("transform", "translate(-1,0)")
    .call(d3.axisRight(y))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick").filter(d => y.domain().includes(d)).remove())
  // Call the chart function to create the plot
  const plot = chart();
  
  // Append the plot to the HTML element with id "contour-plot"
  document.getElementById("contour-plot").appendChild(plot);
  