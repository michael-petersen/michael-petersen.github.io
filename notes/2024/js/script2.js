// Generate random data for the contour plot
const n = 500; // Number of points in each dimension
const data = new Array(n)
    .fill(null)
    .map(() => new Array(n).fill(null).map(() => Math.random() * 10));

// Create a D3 contour generator
const contour = d3.contourDensity()
    .size([500, 500])
    .bandwidth(10)
    .thresholds(20); // Number of contour lines

// Calculate contours from the random data
const contours = contour(data);

console.log(contours);

// Define the color scale
const colorScale = d3.scaleSequential(d3.interpolateViridis)
    .domain([d3.min(contours, d => d.value), d3.max(contours, d => d.value)]);

// Calculate the bounding box of the contours manually
let minX = -500.0;
let maxX = 500.0;
let minY = -500.0;
let maxY = 500.0;

// Calculate the scale and translate to fit the entire matrix
const scale = 10*Math.min(500 / (maxX - minX), 500 / (maxY - minY));
const translateX = -minX * scale + (500 - (maxX - minX) * scale) / 2;
const translateY = -minY * scale + (500 - (maxY - minY) * scale) / 2;


console.log(scale);
console.log(translateX);

// Append an SVG element with correct scaling and translation
const svg = d3.select("#contour-svg")
    .attr("width", 500)
    .attr("height", 500)
    .append("g")
    .attr("transform", `translate(${translateX}, ${translateY}) scale(${scale})`);

// Append paths for each contour line
svg.selectAll("path")
    .data(contours)
    .enter().append("path")
    .attr("d", d3.geoPath())
    .attr("fill", d => colorScale(d.value))
    .attr("stroke", "black");

// Add labels for the contours
svg.selectAll("text")
    .data(contours)
    .enter().append("text")
    .attr("x", d => d.coordinates[0][0][0])
    .attr("y", d => d.coordinates[0][0][1])
    .text(d => d.value.toFixed(1))
    .attr("dy", "0.35em")
    .style("font-size", "10px")
    .style("fill", "black");

