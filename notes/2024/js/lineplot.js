

function create2DGaussian(width, height, centerX, centerY, sigmaX, sigmaY, amplitude) {
    const matrix = [];
    for (let y = 0; y < height; y++) {
        const row = [];
        for (let x = 0; x < width; x++) {
            const exponent = -(
                Math.pow(x - centerX, 2) / (2 * Math.pow(sigmaX, 2)) +
                Math.pow(y - centerY, 2) / (2 * Math.pow(sigmaY, 2))
            );
            const value = amplitude * Math.exp(exponent);
            row.push(value);
        }
        matrix.push(row);
    }
    return matrix;
}


// Parameters for the Gaussian
const gwidth = 100;
const gheight = 100;
const gcenterX = gwidth / 2;
const gcenterY = gheight / 2;
const gsigmaX = 10;
const gsigmaY = 4;
const gamplitude = 10;

// Create the 2D Gaussian matrix
const gaussianMatrix = create2DGaussian(gwidth, gheight, gcenterX, gcenterY, gsigmaX, gsigmaY, gamplitude);



// Sample data: a row of a matrix
const rowData = gaussianMatrix[50];

// Set margins and dimensions for the plot
const margin = { top: 20, right: 20, bottom: 30, left: 40 };
const width = 500 - margin.left - margin.right;
const height = 300 - margin.top - margin.bottom;

// Create SVG element
const svg = d3.select("#line-plot")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("style", "max-width: 100%; height: auto;")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Set x scale
const x = d3.scaleLinear()
    .domain([0, rowData.length - 1])
    .range([0, width]);

// Set y scale
const y = d3.scaleLinear()
    .domain([0, d3.max(rowData)])
    .range([height, 0]);

// Create a line function
const line = d3.line()
    .x((d, i) => x(i))
    .y(d => y(d));

// Append the line to the SVG
svg.append("path")
    .datum(rowData)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2)
    .attr("d", line);

// Add x axis
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

// Add y axis
svg.append("g")
    .call(d3.axisLeft(y));
