
// TO READ on d3
// https://www.d3indepth.com/selections/
// https://bl.ocks.org/d3indepth/cd21d0522fc6f48e3fb88c7f770eb008
// cool axis labels: https://observablehq.com/@d3/scatterplot
// colours: https://github.com/d3/d3-scale-chromatic
// legends: https://bl.ocks.org/zanarmstrong/0b6276e033142ce95f7f374e20f1c1a7
// lines: https://www.d3-graph-gallery.com/graph/line_basic.html


// -------------------------------------------------------------------------------
// define the axes scales: these are generic for all figures
var chartDiv = document.getElementById("chart");

var margin = {top: 20, right: 40, bottom: 70, left: 60},
    width = 0.8*chartDiv.clientWidth - margin.left - margin.right,
    height = 0.8*chartDiv.clientWidth/(16/9) - margin.top - margin.bottom;
// -------------------------------------------------------------------------------


// -------------------------------------------------------------------------------
// add Figure 1
var fig2 = d3.select("#two")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top +")");

// set up x
var xValue2 = function(d) { return d.sigma;},
    xScale2 = d3.scaleLog().domain([1,15]).range([0, width])
    xMap2 = function(d) { return xScale2(xValue2(d));},
    xAxis2 = d3.axisBottom(xScale2).ticks(10, "~s");

// set up y
var yValue2 = function(d) { return d.sigFeH;},
    yScale2 = d3.scaleLinear().domain([0,0.9]).range([height, 0]),
    yMap2 = function(d) { return yScale2(yValue2(d));},
    yAxis2 = d3.axisLeft(yScale2);

// set up colors
// done in figures.js

// Handmade legend
// https://d3-graph-gallery.com/graph/custom_legend.html
//fig2.append("circle").attr("cx",100).attr("cy",10).attr("r", 2.5).style("fill", "white").attr("class", "dot1a")
//fig2.append("text").attr("x", 120).attr("y", 10).text("Globular Clusters (Harris 2010)").style("font-size", "15px").attr("alignment-baseline","middle")
//fig2.append("circle").attr("cx",100).attr("cy",30).attr("r", 5.5).style("fill", colorscale2(0.8))
//fig2.append("text").attr("x", 120).attr("y", 30).text("Newly discovered Ultrafaints (Cerny 2022a,b, Heiger 2023)").style("font-size", "15px").attr("alignment-baseline","middle")
//fig2.append("circle").attr("cx",100).attr("cy",50).attr("r", 5.5).style("fill", colorscale2(0.4))
//////fig2.append("text").attr("x", 120).attr("y", 50).text("LMC associations (Erkal & Belokurov 2020)").style("font-size", "15px").attr("alignment-baseline","middle")
//fig2.append("circle").attr("cx",100).attr("cy",70).attr("r", 5.5).style("fill", colorscale1(0.8))
//fig2.append("text").attr("x", 120).attr("y", 70).text("Classical dwarfs (Simon 2019)").style("font-size", "15px").attr("alignment-baseline","middle")
//fig2.append("circle").attr("cx",100).attr("cy",90).attr("r", 5.5).style("fill", colorscale1(0.2))
//fig2.append("text").attr("x", 120).attr("y", 90).text("Ultrafaint dwarfs (Simon 2019)").style("font-size", "15px").attr("alignment-baseline","middle")


var gravG = 0.0000043009125; // gravitational constant, (km/s)^2 * kpc / Msun


// add the mouseover feature to the page
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip").style("opacity", 0);

var tooltip2 = d3.select("#two").append("div")
    .attr("class", "tooltip").style("opacity", 0);


// start the data access
d3.csv("streams.csv",d3.autoType).then( function(sdata){
    sdata.forEach(function(d) {
      // convert data into numbers
      d.ddhel         = +d.ddhel
      d.dhel          = +d.dhel
      d.udhel         = +d.uudhel
      d.sigma       = Math.min(d.sigma,1000)
      d.usigma      = Math.max(d.udsig,.01)
      d.dsigma      = Math.min(d.ddsig,-.01)
      d.sigFeH      = +d.sigFeH
      d.usigFeH    = +d.usigFeH
      d.dsigFeH    = +d.dsigFeH
    });
  
    // print example data to console for checking
    console.log(sdata[0]);

    // draw dots, and make them mouseable
    fig2.selectAll(".dot")
        .data(sdata)
        .enter().append("circle")
        .attr("class", "dot1a")
        .attr("r", 2.5)
        .attr("cx", xMap2)
        .attr("cy", yMap2)
    	.style("fill", "white")
        .on("mouseover", function(d) {
            tooltip.transition().duration(200).style("opacity", .9);
            tooltip.html(d['stream'] + "<br/> (sv=" + xValue2(d)
              + "km/s , sFeH=" + yValue2(d) + "dex)")
                 .style("left", (d3.event.pageX + 5) + "px")
                 .style("top", (d3.event.pageY - 28) + "px");
            })
        .on("mouseout", function(d) {
            tooltip.transition().duration(500).style("opacity", 0);
            });
  
    // draw error bars
    fig2.selectAll('line.xerror')
       .data(sdata)
       .enter().append('line')
       .attr('class', 'xerror')
       .attr('x1', function(d) { return xScale2(d.sigma+d.dsigma); })
       .attr('x2', function(d) { return xScale2(d.sigma+d.usigma); })
       .attr('y1', function(d) { return yScale2(d.sigFeH); })
       .attr('y2', function(d) { return yScale2(d.sigFeH); });
  
    fig2.selectAll('line.yerror')
       .data(sdata)
       .enter().append('line')
       .attr('class', 'yerror')
       .attr('x1', function(d) { return xScale2(d.sigma); })
       .attr('x2', function(d) { return xScale2(d.sigma); })
       .attr('y1', function(d) { return yScale2(d.sigFeH+d.dsigFeH); })
       .attr('y2', function(d) { return yScale2(d.sigFeH+d.usigFeH); });
  
  }); // end streams data
  

// start the data access
d3.csv("simondwarfs.csv",d3.autoType).then( function(data){
  data.forEach(function(d) {
    // convert data into numbers
    d.dr2         = +d.dr2
    d.r2          = +d.r2
    d.ur2         = +d.ur2
    d.MV          = +d.MV
    d.uMV         = +d.uMV
    d.dMV         = +d.dMV
    d.Vhel        = +d.Vhel
    d.uVhel       = +d.uVhel
    d.dVhel       = +d.dVhel
    d.sigma       = Math.min(d.sigma,1000)
    d.usigma      = Math.max(d.udsig,.01)
    d.dsigma      = Math.min(d.ddsig,-.01)
    d.luminosity  = Math.pow(10., (+d.MV - 4.77)/-2.5) + 1.
    d.dluminosity = Math.pow(10., (+d.MV+d.dMV - 4.77)/-2.5)
    d.uluminosity = Math.pow(10., (+d.MV+d.uMV - 4.77)/-2.5)
    d.mhalf       = (5.*0.001*+d.r2*+d.sigma*+d.sigma)/(2*gravG) // equation 7 of penarrubia 2016
    d.umhalf      = 5.*0.001*(+d.r2+d.dr2)*(+d.sigma+d.usigma)*(+d.sigma+d.usigma)/(2*gravG)
    d.dmhalf      = 5.*0.001*(+d.r2+d.ur2)*(+d.sigma+d.dsigma)*(+d.sigma+d.dsigma)/(2*gravG)
    //console.log(d.mhalf,d.umhalf,d.r2+d.dr2,d.sigma+d.dsigma)
    d.sigFeH      = +d.sigFeH
    d.usigFeH    = +d.usigFeH
    d.dsigFeH    = +d.dsigFeH
    d.masslum     = d.mhalf/d.luminosity
    d.umasslum    = (+d.mhalf+d.umhalf)/d.luminosity
    d.dmasslum    = (+d.mhalf+d.dmhalf)/d.luminosity
  });

  // print example data to console for checking
  //console.log(data[0].mhalf+data[0].umhalf);
  //console.log(data[0].MV+data[0].dMV);

  // if specific datacut is desired...
  //groupFourData = data.filter(function(d) { return d.year == 1946 })

  // x-axis
  fig2.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis2)
      .style("font-size", "15px")
  fig2.append("text")
      .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 20) + ")")
      .style("text-anchor", "middle")
      .style("font-size", "15px")
      .text("Velocity dispersion (km/s)");

  // y-axis
  fig2.append("g")
      .attr("class", "y axis")
      .call(yAxis2)
      .style("font-size", "15px")
  fig2.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .style("font-size", "15px")
      .text("Metallicity dispersion (dex)");

  // draw dots, and make them mouseable
  fig2.selectAll(".dot")
      .data(data)
      .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5.5)
      .attr("cx", xMap2)
      .attr("cy", yMap2)
      .style("fill", function(d) { return cValue1(d);})
      .on("mouseover", function(d) {
          tooltip.transition().duration(200).style("opacity", .9);
          tooltip.html(d['Dwarf'] + "<br/> (sv=" + xValue2(d)
	        + "km/s , sFeH=" + yValue2(d) + "dex)")
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
          })
      .on("mouseout", function(d) {
          tooltip.transition().duration(500).style("opacity", 0);
          });

  // draw error bars
  fig2.selectAll('line.xerror')
     .data(data)
     .enter().append('line')
     .attr('class', 'xerror')
     .attr('x1', function(d) { return xScale2(d.sigma+d.dsigma); })
     .attr('x2', function(d) { return xScale2(d.sigma+d.usigma); })
     .attr('y1', function(d) { return yScale2(d.sigFeH); })
     .attr('y2', function(d) { return yScale2(d.sigFeH); });

  fig2.selectAll('line.yerror')
     .data(data)
     .enter().append('line')
     .attr('class', 'yerror')
     .attr('x1', function(d) { return xScale2(d.sigma); })
     .attr('x2', function(d) { return xScale2(d.sigma); })
     .attr('y1', function(d) { return yScale2(d.sigFeH+d.dsigFeH); })
     .attr('y2', function(d) { return yScale2(d.sigFeH+d.usigFeH); });

}); // end simondwarfs data
