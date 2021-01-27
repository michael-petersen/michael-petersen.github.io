
// TO READ on d3
// https://www.d3indepth.com/selections/
// https://bl.ocks.org/d3indepth/cd21d0522fc6f48e3fb88c7f770eb008
// cool axis labels: https://observablehq.com/@d3/scatterplot
// colours: https://github.com/d3/d3-scale-chromatic
// legends: https://bl.ocks.org/zanarmstrong/0b6276e033142ce95f7f374e20f1c1a7
// lines: https://www.d3-graph-gallery.com/graph/line_basic.html



// define the axes scales
var chartDiv = document.getElementById("chart");

var margin = {top: 20, right: 40, bottom: 70, left: 60},
    width = 0.8*chartDiv.clientWidth - margin.left - margin.right,
    height = 0.8*chartDiv.clientWidth/(2/1) - margin.top - margin.bottom;

// add Figure 1
var fig1 = d3.select("#one")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top +")");

// setup x 
var xValue1 = function(d) { return d.Sigma;},
    xScale1 = d3.scaleLog().domain([16,400]).range([0, width])
    xMap1 = function(d) { return xScale1(xValue1(d));},
    xAxis1 = d3.axisBottom(xScale1).ticks(10, "~s");

// setup y
var yValue1 = function(d) { return d.MBH;},
    //yScale1 = d3.scaleLinear().domain([0,-14]).range([height, 0]),
    yScale1 = d3.scaleLog().domain([5000,100000000000]).range([height, 0]),
    yMap1 = function(d) { return yScale1(yValue1(d));},
    yAxis1 = d3.axisLeft(yScale1);


// setup colors
var colorscale1 = d3.scaleSequential(d3.interpolateBlues).domain([0,1]),
    cValue1 = function(d) { if      (d.HT=="E")  {return colorscale1(0.9);}
			    else if (d.HT=="S0") {return colorscale1(0.45);}
			    else if (d.HT=="S")  {return colorscale1(0.2);}
			    else                 {return colorscale1(1.0);}};

// u.dsig



// add the mouseover feature to the page
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip").style("opacity", 0);

var tooltip6 = d3.select("#six").append("div")
    .attr("class", "tooltip").style("opacity", 0);

var tooltip1 = d3.select("#one").append("div")
    .attr("class", "tooltip").style("opacity", 0);



// start the data access
d3.csv("greene.csv",d3.autoType).then( function(data){
  data.forEach(function(d) {
    // convert data into numbers
    d.Sigma = +d.Sigma
    d.MBH = +d.MBH
      console.log(d.Sigma,d.MBH,d.HT)
  });

  // x-axis
  fig1.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis1)
  fig1.append("text")
      .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("log Velocity Dispersion (km/s)");

  // y-axis
  fig1.append("g")
      .attr("class", "y axis")
      .call(yAxis1)
  fig1.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("MBH (Msun)");

  // draw dots
  fig1.selectAll(".dot")
      .data(data)
      .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5.5)
      .attr("cx", xMap1)
      .attr("cy", yMap1)
      .style("fill", function(d) { return cValue1(d);}) 
      .on("mouseover", function(d) {
          tooltip.transition().duration(200).style("opacity", .9);
          tooltip.html(d['Galaxy'] + "<br/> (" + d['Distance'] 
	        + "Mpc)")
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
          })
      .on("mouseout", function(d) {
          tooltip.transition().duration(500).style("opacity", 0);
          });

 
  // draw error bars
  fig1.selectAll('line.xerror')
     .data(data)
     .enter().append('line')
     .attr('class', 'xerror')
     .attr('x1', function(d) { return xScale1(d.r2+d.dr2); })
     .attr('x2', function(d) { return xScale1(d.r2+d.ur2); })
     .attr('y1', function(d) { return yScale1(d.MV); })
     .attr('y2', function(d) { return yScale1(d.MV); });

  fig1.selectAll('line.yerror')
     .data(data)
     .enter().append('line')
     .attr('class', 'yerror')
     .attr('x1', function(d) { return xScale1(d.r2); })
     .attr('x2', function(d) { return xScale1(d.r2); })
     .attr('y1', function(d) { return yScale1(d.MV+d.dMV); })
     .attr('y2', function(d) { return yScale1(d.MV+d.uMV); });



});


