
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
var fig1 = d3.select("#one")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top +")");

// set up x
var xValue1 = function(d) { return d.r2;},
    xScale1 = d3.scaleLog().domain([0.8,3000]).range([0, width])
    xMap1 = function(d) { return xScale1(xValue1(d));},
    xAxis1 = d3.axisBottom(xScale1).ticks(10, "~s");

// set up y
var yValue1 = function(d) { return d.MV;},
    yScale1 = d3.scaleLinear().domain([1,-14]).range([height, 0]),
    yMap1 = function(d) { return yScale1(yValue1(d));},
    yAxis1 = d3.axisLeft(yScale1);


// set up colors
var colorscale1 = d3.scaleSequential(d3.interpolateBlues).domain([0,1]),
    colorscale2 = d3.scaleSequential(d3.interpolateReds).domain([0,1]),
    cValue1 = function(d) {
      if ( d.Dwarf=="Pegasus IV" || d.Dwarf=="Delve 3" || d.Dwarf=="Delve 4" || d.Dwarf=="Virgo II" || d.Dwarf=="Delve 5" || d.Dwarf=="Bootes V" || d.Dwarf=="Leo Minor I")
        { return colorscale2(0.8);}
      else if (d.Dwarf=="Carina II" || d.Dwarf=="Carina III" || d.Dwarf=="Horologium I" || d.Dwarf=="Hydrus I" || d.Dwarf=="Phoenix II" || d.Dwarf=="Reticulum II")
        { return colorscale2(0.4);}
      else if (d.MV>-7.5)
        { return colorscale1(0.2);}
			else
        { return colorscale1(0.8);}
      },

    cValue2 = function(d) {
          if (d.udsig==0)
            { return colorscale2(0.2);}
			    else if ( d.Dwarf=="Segue 1" || d.Dwarf=="Antlia 2")
            { return colorscale2(0.5);}
          else if (d.MV>-7.5)
            { return colorscale1(0.2);}
			    else
            { return colorscale1(0.8);}
          };


var gravG = 0.0000043009125; // gravitational constant, (km/s)^2 * kpc / Msun


// add the mouseover feature to the page
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip").style("opacity", 0);

var tooltip1 = d3.select("#one").append("div")
    .attr("class", "tooltip").style("opacity", 0);


    // start the data access for GCs
    d3.csv("harris10.csv",d3.autoType).then( function(data){
      data.forEach(function(d) {
        // convert data into numbers
        d.MV = +d.MV
        d.r2 = +d.rhalf
        d.appmag = +d.vmag
          d.dist = +d.helio_distance
          d.sigma = +d.sigma
      });

      // print example data to console for checking
      console.log(data[0]);

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

    });


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

  // draw dots, and make them mouseable
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

}); // end simondwarfs data
