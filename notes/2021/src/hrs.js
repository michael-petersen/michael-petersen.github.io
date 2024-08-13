// start here:
// https://www.d3-graph-gallery.com/graph/line_change_data.html

// AL-specific HR data
var data1 = [
  {"year": 2004,    "hrs": 2605},
  {"year": 2005,    "hrs": 2437},
  {"year": 2006,    "hrs": 2546},
  {"year": 2007,    "hrs": 2252},
  {"year": 2008,    "hrs": 2270},
  {"year": 2009,    "hrs": 2560},
  {"year": 2010,    "hrs": 2209},
  {"year": 2011,    "hrs": 2271},
  {"year": 2012,    "hrs": 2500},
  {"year": 2013,    "hrs": 2504},
  {"year": 2014,    "hrs": 2161},
  {"year": 2015,    "hrs": 2634},
  {"year": 2016,    "hrs": 2953},
  {"year": 2017,    "hrs": 3170},
  {"year": 2018,    "hrs": 2900},
  {"year": 2019,    "hrs": 3478},
  {"year": 2020,    "hrs": 3086},
  {"year": 2021,    "hrs": 3059},
]

// NL-specific HR data
var data2 = [
  {"year": 2004,    "hrs": 2846},
  {"year": 2005,    "hrs": 2580},
  {"year": 2006,    "hrs": 2840},
  {"year": 2007,    "hrs": 2705},
  {"year": 2008,    "hrs": 2608},
  {"year": 2009,    "hrs": 2482},
  {"year": 2010,    "hrs": 2404},
  {"year": 2011,    "hrs": 2281},
  {"year": 2012,    "hrs": 2434},
  {"year": 2013,    "hrs": 2157},
  {"year": 2014,    "hrs": 2025},
  {"year": 2015,    "hrs": 2275},
  {"year": 2016,    "hrs": 2657},
  {"year": 2017,    "hrs": 2935},
  {"year": 2018,    "hrs": 2685},
  {"year": 2019,    "hrs": 3298},
  {"year": 2020,    "hrs": 3135},
  {"year": 2021,    "hrs": 2885},
]

// set the dimensions and margins of the graph:
// already set by the other graph, so we'll leave this alone!
//const margin = {top: 10, right: 30, bottom: 30, left: 60},
//    width = 860 - margin.left - margin.right,
//    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg2 = d3.select("#chart2")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Add X axis --> it is a date format
const x2 = d3.scaleTime()
  .range([ 0, width ]);
const xAxis = d3.axisBottom().scale(x2);
svg2.append("g")
  .attr("transform", `translate(0, ${height})`)
  .attr("class","myXaxis");

// Add Y axis
const y2 = d3.scaleLinear()
  .range([ height, 0 ]);
const yAxis = d3.axisLeft().scale(y2);
svg2.append("g")
  .attr("class","myYaxis");


  // text label for the x axis
svg2.append("text")
    .attr("x", width/2 + margin.left - 10)
    .attr("y", height + margin.top + 20)
    .style("text-anchor", "end")
    .text("year");

  // text label for the y axis
svg2.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", - margin.left + 20)
    .attr("x", - margin.top - height/2 + 50)
    .style("text-anchor", "end")
    .text("homeruns");


// Create a function that takes a dataset as input and update the plot:
function update(data) {

  // Create the X axis:
  x2.domain(d3.extent(data.map(function(d) { return d3.timeParse("%Y")(d.year); })));
  svg2.selectAll(".myXaxis").transition()
    .duration(2000)
    .call(xAxis);

  // create the Y axis
  y2.domain([d3.min(data.map(function(d) { return +d.hrs; })),d3.max(data.map(function(d) { return +d.hrs; }))]);
  svg2.selectAll(".myYaxis")
    .transition()
    .duration(3000)
    .call(yAxis);

  // Create a update selection: bind to the new data
  const u = svg2.selectAll(".lineTest")
    .data([data], function(d){ return d3.timeParse("%Y")(d.year); });

  // Updata the line
  u
    .join("path")
    .attr("class","lineTest")
    .transition()
    .duration(3000)
    .attr("d", d3.line()
      .x(function(d) { return x2(d3.timeParse("%Y")(d.year)); })
      .y(function(d) { return y2(+d.hrs); }))
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2.5)
}

// At the beginning, I run the update function on the first dataset:
update(data1)
