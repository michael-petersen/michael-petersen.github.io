
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

value = (x, y) => Math.sin(x + y) * Math.sin(x - y)

chart = {
    const context = DOM.context2d(width, height);
    const path = d3.geoPath(null, context);
    context.scale(width / (grid.n - 1), width / (grid.n - 1));
    context.translate(-0.5, -0.5);
    while (true) {
      const dv = (Date.now() % 1000) / 1000 * 0.2;
      for (const v of thresholds) {
        context.beginPath();
        path(contours.contour(grid, v + dv));
        context.fillStyle = color(v + dv);
        context.fill();
      }
      yield context.canvas;
    }
  }


// Append the SVG element.
container.append(svg.node());
