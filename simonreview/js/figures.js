
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
    height = 0.8*chartDiv.clientWidth/(16/9) - margin.top - margin.bottom;

// add Figure 1
var fig1 = d3.select("#one")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top +")");

// setup x 
var xValue1 = function(d) { return d.r2;},
    xScale1 = d3.scaleLog().domain([0.8,3000]).range([0, width])
    xMap1 = function(d) { return xScale1(xValue1(d));},
    xAxis1 = d3.axisBottom(xScale1).ticks(10, "~s");

// setup y
var yValue1 = function(d) { return d.MV;},
    yScale1 = d3.scaleLinear().domain([0,-14]).range([height, 0]),
    yMap1 = function(d) { return yScale1(yValue1(d));},
    yAxis1 = d3.axisLeft(yScale1);


// setup colors
var colorscale1 = d3.scaleSequential(d3.interpolateBlues).domain([0,1]),
    colorscale2 = d3.scaleSequential(d3.interpolateReds).domain([0,1]),
    cValue1 = function(d) { if ( d.Dwarf=="Segue 1" ||
				 //d.Dwarf=="Sagittarius II" ||
				 d.Dwarf=="Antlia 2") {return colorscale2(0.5);}
                       else if (d.MV>-7.5) {return colorscale1(0.2);}
			    else { return colorscale1(0.8);}};

    cValue2 = function(d) { if (d.udsig==0) {return colorscale2(0.2);}
			    else if ( d.Dwarf=="Segue 1" ||
				      //d.Dwarf=="Sagittarius II" ||
				      d.Dwarf=="Antlia 2") {return colorscale2(0.5);}
                       else if (d.MV>-7.5) {return colorscale1(0.2);}
			    else { return colorscale1(0.8);}};
// u.dsig

// ------------------------------------------------------------------------------------
// add Figure 2
var fig2 = d3.select("#two").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// setup x 
var xValue2 = function(d) { return d.MV;},
    xScale2 = d3.scaleLinear().domain([0,-14]).range([0, width])
    xMap2 = function(d) { return xScale2(xValue2(d));},
xAxis2 = d3.axisBottom(xScale2);

var xValue2 = function(d) { return d.r2;},
    xScale2 = d3.scaleLog().domain([10,3000]).range([0, width])
    xMap2 = function(d) { return xScale2(xValue2(d));},
    xAxis2 = d3.axisBottom(xScale2).ticks(10, "~s");

// setup y
var yValue2 = function(d) { return d.sigma;},
    yScale2 = d3.scaleLinear().domain([0,12]).range([height, 0]),
    yMap2 = function(d) { return yScale2(yValue2(d));},
yAxis2 = d3.axisLeft(yScale2);

// ------------------------------------------------------------------------------------
// add Figure 3
var fig3 = d3.select("#three").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// setup x 
var xValue3 = function(d) { return d.dist;},
    xScale3 = d3.scaleLinear().domain([0,500]).range([0, width])
    xMap3 = function(d) { return xScale3(xValue3(d));},
    xAxis3 = d3.axisBottom(xScale3);

// setup y
var yValue3 = function(d) { return d.appmag;},
    yScale3 = d3.scaleLinear().domain([3,25]).range([height, 0]),
    yMap3 = function(d) { return yScale3(yValue3(d));},
    yAxis3 = d3.axisLeft(yScale3);


// ------------------------------------------------------------------------------------
// add Figure 4
var fig4 = d3.select("#four").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// setup x 
var xValue4 = function(d) { return d.luminosity;},
    xScale4 = d3.scaleLog().domain([50,50000000]).range([0, width])
    xMap4 = function(d) { return xScale4(xValue4(d));},
    xAxis4 = d3.axisBottom(xScale4).ticks(10, "~s");

// setup y
var yValue4 = function(d) { return d.mhalf;},
    yScale4 = d3.scaleLog().domain([10000,1000000000]).range([height, 0]),
    yMap4 = function(d) { return yScale4(yValue4(d));},
    yAxis4 = d3.axisLeft(yScale4).ticks(6, "~s");

// ------------------------------------------------------------------------------------
// add Figure 5
var fig5 = d3.select("#five").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// setup x 
var xValue5 = function(d) { return d.luminosity;},
    xScale5 = d3.scaleLog().domain([50,50000000]).range([0, width])
    xMap5 = function(d) { return xScale5(xValue5(d));},
    xAxis5 = d3.axisBottom(xScale5).ticks(10, "~s");

// setup y
var yValue5 = function(d) { return d.masslum;},
    yScale5 = d3.scaleLog().domain([1,10000]).range([height, 0]),
    yMap5 = function(d) { return yScale5(yValue5(d));},
    yAxis5 = d3.axisLeft(yScale5).ticks(4, "~s");

// ------------------------------------------------------------------------------------
// add Figure 6
var fig6 = d3.select("#six").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// setup x 
var xValue6 = function(d) { return d.dmw;},
    xScale6 = d3.scaleLinear().domain([0,600]).range([0, width])
    xMap6 = function(d) { return xScale6(xValue6(d));},
    xAxis6 = d3.axisBottom(xScale6).ticks(10);

// setup y
var yValue6 = function(d) { return d.vmw;},
    yScale6 = d3.scaleLinear().domain([0,500]).range([height, 0]),
    yMap6 = function(d) { return yScale6(yValue6(d));},
    yAxis6 = d3.axisLeft(yScale6).ticks(4);



var gravG = 0.0000043009125; // gravitational constant, (km/s)^2 * kpc / Msun




// add the mouseover feature to the page
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip").style("opacity", 0);

var tooltip6 = d3.select("#six").append("div")
    .attr("class", "tooltip").style("opacity", 0);

var tooltip1 = d3.select("#one").append("div")
    .attr("class", "tooltip").style("opacity", 0);


// start the data access for LG satellites
d3.csv("weisz19.csv").then( function(data){
  data.forEach(function(d) {
    // convert data into numbers
    d.dm31 = +d.dm31
      d.MV = +d.MV
      d.r2 = +d.hlight
  });

  // print example data to console for checking
    //console.log(data[0]);

  // draw dots
  fig1.selectAll(".dot")
      .data(data)
      .enter().append("circle")
      .attr("class", "dot1a")
      .attr("r", 4.5)
      .attr("cx", xMap1)
      .attr("cy", yMap1)
.style("fill", "silver")
    .on("mouseover", function(d) {
          tooltip1.transition().duration(200).style("opacity", .9);
          tooltip1.html(d['name'])
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
          })
      .on("mouseout", function(d) {
          tooltip1.transition().duration(500).style("opacity", 0);
          });
});




// start the data access for LG satellites
d3.csv("mconnachie12_2.csv",d3.autoType).then( function(data){
  data.forEach(function(d) {
    // convert data into numbers
    d.dmw = +d.dmw
      d.vmw = Math.sqrt(3 * d.vmw*d.vmw)
  });

  // print example data to console for checking
    console.log(data);


  // x-axis
  fig6.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis6)
  fig6.append("text")
      .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("MW Distance [kpc]");

  // y-axis
  fig6.append("g")
      .attr("class", "y axis")
      .call(yAxis6)
  fig6.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("MW Velocity [km/s]");


var datal = [{x: 10}, {x: 100}, {x: 300}, {x: 500}]

// create svg element:
var svg = d3.select("#curve").append("svg").attr("width", 800).attr("height", 200)

// prepare a helper function
var curveFunc1 = d3.line()
  .curve(d3.curveBasis)              // This is where you define the type of curve. Try curveStep for instance.
  .x(function(d) { return xScale3(d.x) })
    .y(function(d) {  return yScale6(Math.sqrt((2*gravG*1.e12)/d.x)) })


// Add the path using this helper function
fig6.append('path')
  .attr('d', curveFunc1(datal))
  .attr('stroke', '#f0c1cb')
  .attr('stroke-width', '2pt')
  .attr('fill', 'none');


  // draw dots
  fig6.selectAll(".dot")
      .data(data)
      .enter().append("circle")
      .attr("class", "dot1a")
      .attr("r", 4.5)
      .attr("cx", xMap6)
      .attr("cy", yMap6)
.style("fill", "white")
      .on("mouseover", function(d) {
          tooltip6.transition().duration(200).style("opacity", .9);
          tooltip6.html(d['name'])
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
          })
      .on("mouseout", function(d) {
          tooltip6.transition().duration(500).style("opacity", 0);
          });


});



// start the data access for LG satellites
d3.csv("updatedsatellites.csv",d3.autoType).then( function(data){
  data.forEach(function(d) {
    // convert data into numbers
      d.dmw = Math.sqrt(d.x*d.x + d.y*d.y + d.z*d.z)
      d.vmw = Math.sqrt(d.vx*d.vx + d.vy*d.vy + d.vz*d.vz) 
  });

  // print example data to console for checking
    //console.log(data[0]);


  // x-axis
  fig6.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis6)
  fig6.append("text")
      .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("MW Distance [kpc]");

  // y-axis
  fig6.append("g")
      .attr("class", "y axis")
      .call(yAxis6)
  fig6.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("MW Velocity [km/s]");

    
  // draw dots
  fig6.selectAll(".dot")
      .data(data)
      .enter().append("circle")
      .attr("class", "dot1a")
      .attr("r", 4.5)
      .attr("cx", xMap6)
      .attr("cy", yMap6)
.style("fill", "silver")
      .on("mouseover", function(d) {
          tooltip6.transition().duration(200).style("opacity", .9);
          tooltip6.html(d['name'])
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
          })
      .on("mouseout", function(d) {
          tooltip6.transition().duration(500).style("opacity", 0);
          });


});




// start the data access for GCs
d3.csv("harris10.csv",d3.autoType).then( function(data){
  data.forEach(function(d) {
    // convert data into numbers
    d.MV = +d.MV
    d.r2 = +d.rhalf
    d.appmag = +d.vmag
      d.dist = +d.helio_distance
  });

  // print example data to console for checking
//console.log(data[0]);

gdata = data.filter(function(d) { return d.MV < 0. })

//console.log(data[0]['name']);

// https://www.d3-graph-gallery.com/graph/shape.html
// http://bl.ocks.org/enthal/1726550
var datal = [{x: 10}, {x: 100}, {x: 300}, {x: 500}]

// create svg element:
var svg = d3.select("#curve").append("svg").attr("width", 800).attr("height", 200)

// prepare a helper function
var curveFunc1 = d3.line()
  .curve(d3.curveBasis)              // This is where you define the type of curve. Try curveStep for instance.
  .x(function(d) { return xScale3(d.x) })
  .y(function(d) { return yScale3(5*Math.log10(d.x)+2.7) })

var curveFunc2 = d3.line()
  .curve(d3.curveBasis)              // This is where you define the type of curve. Try curveStep for instance.
  .x(function(d) { return xScale3(d.x) })
  .y(function(d) { return yScale3(5*Math.log10(d.x)+4) })

// Add the path using this helper function
fig3.append('path')
  .attr('d', curveFunc1(datal))
  .attr('stroke', '#f0c1cb')
  .attr('stroke-width', '2pt')
  .attr('fill', 'none');

//fig3.append('path')
//  .attr('d', curveFunc2(datal))
//  .attr('stroke', '#f0c1cb')
//  .attr('stroke-width', '2pt')
//  .attr('fill', 'none');

// lines of faintness
  fig1.selectAll('line1.brightness')
     .data(data)
     .enter().append('line')
     .attr('class', 'brightness')
     .attr('x1', function(d) { return xScale1(1.8); })
     .attr('x2', function(d) { return xScale1(1800.); })
     .attr('y1', function(d) { return yScale1(0.); })
     .attr('y2', function(d) { return yScale1(-14.); });

  fig1.selectAll('line2.brightness')
     .data(data)
     .enter().append('line')
     .attr('class', 'brightness')
     .attr('x1', function(d) { return xScale1(4.5); })
     .attr('x2', function(d) { return xScale1(3000.); })
     .attr('y1', function(d) { return yScale1(0.); })
     .attr('y2', function(d) { return yScale1(-13.25); });

  fig1.selectAll('line3.brightness')
     .data(data)
     .enter().append('line')
     .attr('class', 'brightness')
     .attr('x1', function(d) { return xScale1(10.3); })
     .attr('x2', function(d) { return xScale1(3000.); })
     .attr('y1', function(d) { return yScale1(0.); })
     .attr('y2', function(d) { return yScale1(-11.25); });

  fig1.selectAll('line4.brightness')
     .data(data)
     .enter().append('line')
     .attr('class', 'brightness')
     .attr('x1', function(d) { return xScale1(28); })
     .attr('x2', function(d) { return xScale1(3000.); })
     .attr('y1', function(d) { return yScale1(0.); })
     .attr('y2', function(d) { return yScale1(-9.25); });


  // draw dots
  fig1.selectAll(".dot")
      .data(gdata)
      .enter().append("circle")
      .attr("class", "dot1a")
      .attr("r", 2.5)
      .attr("cx", xMap1)
      .attr("cy", yMap1)
	.style("fill", "white")
	.on("mouseover", function(d) {
          tooltip.transition().duration(200).style("opacity", .9);
          tooltip.html(d['name'])
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
          })
      .on("mouseout", function(d) {
          tooltip.transition().duration(500).style("opacity", 0);
          });

  // draw dots
  fig3.selectAll(".dot")
      .data(gdata)
      .enter().append("circle")
      .attr("class", "dot1a")
      .attr("r", 2.5)
      .attr("cx", xMap3)
      .attr("cy", yMap3)
.style("fill", "white")
.on("mouseover", function(d) {
          tooltip.transition().duration(200).style("opacity", .9);
          tooltip.html(d['name'])
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
          })
      .on("mouseout", function(d) {
          tooltip.transition().duration(500).style("opacity", 0);
          });


});




// start the data access
d3.csv("simondwarfs.csv",d3.autoType).then( function(data){
  data.forEach(function(d) {
    // convert data into numbers
    d.dr2 = +d.dr2
    d.r2 = +d.r2
    d.ur2 = +d.ur2
    d.MV = +d.MV
    d.uMV = +d.uMV
    d.dMV = +d.dMV
    d.Vhel = +d.Vhel
    d.uVhel = +d.uVhel
      d.dVhel = +d.dVhel
      d.sigma = Math.min(d.sigma,1000)
      d.usigma = Math.max(d.udsig,.01)
      d.dsigma = Math.min(d.ddsig,-.01)
    d.luminosity = Math.pow(10., (+d.MV - 4.77)/-2.5) + 1.
    d.dluminosity = Math.pow(10., (+d.MV+d.dMV - 4.77)/-2.5)
    d.uluminosity = Math.pow(10., (+d.MV+d.uMV - 4.77)/-2.5)
      d.mhalf = (5.*0.001*+d.r2*+d.sigma*+d.sigma)/(2*gravG) // equation 7 of penarrubia 2016
    d.umhalf = 5.*0.001*(+d.r2+d.dr2)*(+d.sigma+d.usigma)*(+d.sigma+d.usigma)/(2*gravG)
    d.dmhalf = 5.*0.001*(+d.r2+d.ur2)*(+d.sigma+d.dsigma)*(+d.sigma+d.dsigma)/(2*gravG)
      //console.log(d.mhalf,d.umhalf,d.r2+d.dr2,d.sigma+d.dsigma)
    d.masslum = d.mhalf/d.luminosity
    d.umasslum = (+d.mhalf+d.umhalf)/d.luminosity
    d.dmasslum = (+d.mhalf+d.dmhalf)/d.luminosity
  });

  // print example data to console for checking
  console.log(data[0].mhalf+data[0].umhalf);
  console.log(data[0].MV+data[0].dMV);

  // if specific datacut is desired...
  //groupFourData = data.filter(function(d) { return d.year == 1946 })

  // x-axis
  fig1.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis1)
  fig1.append("text")
      .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("Half-Light Radius [pc]");

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
      .text("Absolute V Magnitude");

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
          tooltip.html(d['Dwarf'] + "<br/> (" + xValue1(d) 
	        + "pc , " + yValue1(d) + "mag)")
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


// ------------------------------------------------------------------------------------
// Figure 2
  // x-axis
  fig2.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis2)
  fig2.append("text")
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("Half-Light radius [pc]");

  // y-axis
  fig2.append("g")
      .attr("class", "y axis")
      .call(yAxis2)
fig2.append("text")
.attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Velocity Dispersion [km/s]");

  // draw dots
  fig2.selectAll(".dot")
.data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5.5)
      .attr("cx", xMap2)
      .attr("cy", yMap2)
      .style("fill", function(d) { return cValue2(d);}) 
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", .9);
          tooltip.html(d['Dwarf'] + "<br/> (" + xValue2(d) 
	        + "mag, " + yValue2(d) + "km/s)")
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
});

  // draw error bars
  fig2.selectAll('line.xerror')
     .data(data)
     .enter().append('line')
     .attr('class', 'xerror')
     .attr('x1', function(d) { return xScale2(d.MV+d.dMV); })
     .attr('x2', function(d) { return xScale2(d.MV+d.uMV); })
     .attr('y1', function(d) { return yScale2(d.sigma); })
     .attr('y2', function(d) { return yScale2(d.sigma); });

  fig2.selectAll('line.yerror')
     .data(data)
     .enter().append('line')
     .attr('class', 'yerror')
     .attr('x1', function(d) { return xScale2(d.MV); })
     .attr('x2', function(d) { return xScale2(d.MV); })
     .attr('y1', function(d) { return yScale2(d.sigma+d.dsigma); })
     .attr('y2', function(d) { return yScale2(d.sigma+d.usigma); });

// ------------------------------------------------------------------------------------
// Figure 3
  // x-axis
  fig3.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis3)
  fig3.append("text")
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("Distance [kpc]");

  // y-axis
  fig3.append("g")
      .attr("class", "y axis")
      .call(yAxis3)
fig3.append("text")
.attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Apparent V Magnitude");

  // draw dots
  fig3.selectAll(".dot")
.data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5.5)
      .attr("cx", xMap3)
      .attr("cy", yMap3)
      .style("fill", function(d) { return cValue1(d);}) 
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", .9);
          tooltip.html(d['Dwarf'] + "<br/> (" + xValue3(d) 
	        + "kpc, " + d['MV'] + "mag)")
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
});



// ------------------------------------------------------------------------------------
// Figure 4
  // x-axis
  fig4.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis4)
  fig4.append("text")
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("Luminosity (Lsun)");

  // y-axis
  fig4.append("g")
      .attr("class", "y axis")
      .call(yAxis4)
fig4.append("text")
.attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Mass (Msun)");

  // draw dots
  fig4.selectAll(".dot")
.data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5.5)
      .attr("cx", xMap4)
      .attr("cy", yMap4)
      .style("fill", function(d) { return cValue2(d);}) 
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", .9);
          tooltip.html(d['Dwarf'] + "<br/> (" + d.mhalf.toPrecision(3)
	               + "Msun, " + d.umhalf.toPrecision(3) + "Msun)")
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
});

  // draw error bars
  fig4.selectAll('line.xerror')
     .data(data)
     .enter().append('line')
     .attr('class', 'xerror')
     .attr('x1', function(d) { return xScale4(d.dluminosity); })
     .attr('x2', function(d) { return xScale4(d.uluminosity); })
     .attr('y1', function(d) { return yScale4(d.mhalf); })
     .attr('y2', function(d) { return yScale4(d.mhalf); });

  fig4.selectAll('line.yerror')
     .data(data)
     .enter().append('line')
     .attr('class', 'yerror')
     .attr('x1', function(d) { return xScale4(d.luminosity); })
     .attr('x2', function(d) { return xScale4(d.luminosity); })
     .attr('y1', function(d) { return yScale4(d.dmhalf); })
     .attr('y2', function(d) { return yScale4(d.umhalf); });


    
// ------------------------------------------------------------------------------------
// Figure 5
  // x-axis
  fig5.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis5)
  fig4.append("text")
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .text("Luminosity (Lsun)");

  // y-axis
  fig5.append("g")
      .attr("class", "y axis")
      .call(yAxis5)
fig5.append("text")
.attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Mass-to-Light (Msun/Lsun)");

  // draw dots
  fig5.selectAll(".dot")
.data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5.5)
      .attr("cx", xMap5)
      .attr("cy", yMap5)
      .style("fill", function(d) { return cValue2(d);}) 
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", .9);
          tooltip.html(d['Dwarf'] + "<br/> (" + xValue5(d).toPrecision(3) 
	               + "Lsun, " + yValue5(d).toPrecision(3) + "Msun)")
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
});


});



