// start here:
// https://www.d3-graph-gallery.com/graph/line_basic.html

var data = [
  {"year": 2004,    "sbs": 2589},
  {"year": 2005,    "sbs": 2565},
  {"year": 2006,    "sbs": 2767},
  {"year": 2007,    "sbs": 2918},
  {"year": 2008,    "sbs": 2799},
  {"year": 2009,    "sbs": 2970},
  {"year": 2010,    "sbs": 2959},
  {"year": 2011,    "sbs": 3279},
  {"year": 2012,    "sbs": 3229},
  {"year": 2013,    "sbs": 2693},
  {"year": 2014,    "sbs": 2764},
  {"year": 2015,    "sbs": 2505},
  {"year": 2016,    "sbs": 2537},
  {"year": 2017,    "sbs": 2527},
  {"year": 2018,    "sbs": 2474},
  {"year": 2019,    "sbs": 2280},
  {"year": 2020,    "sbs": 2389},
  {"year": 2021,    "sbs": 2213},
]

// set the dimensions and margins of the graph
const margin = {top: 10, right: 30, bottom: 50, left: 60},
    width = 860 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#chart1")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Add X axis --> it is a date format
const x = d3.scaleTime()
  .domain(d3.extent(data.map(function(d) { return d3.timeParse("%Y")(d.year); })))
  .range([ 0, width ]);
svg.append("g")
  .attr("transform", `translate(0, ${height})`)
  .call(d3.axisBottom(x));

// Add Y axis
const y = d3.scaleLinear()
  .domain([d3.min(data.map(function(d) { return +d.sbs; })),d3.max(data.map(function(d) { return +d.sbs; }))])
  .range([ height, 0 ]);
svg.append("g")
  .call(d3.axisLeft(y));

// Add the line
svg.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "steelblue")
  .attr("stroke-width", 1.5)
  .attr("d", d3.line()
    .x(function(d) { return x(d3.timeParse("%Y")(d.year)) })
    .y(function(d) { return y(d.sbs) }))

// text label for the x axis
svg.append("text")
  .attr("x", width/2 + margin.left - 10)
  .attr("y", height + margin.top + 20)
  .style("text-anchor", "end")
  .text("year");

// text label for the y axis
svg.append("text")
  .attr("transform", "rotate(-90)")
  .attr("y", - margin.left + 20)
  .attr("x", - margin.top - height/2 + 50)
  //.attr("dy", "1em")
  .style("text-anchor", "end")
  .text("stolen bases");
