function getValues()
{
var distance      = document.getElementById('distance').value;
var linearterm    = document.getElementById('linear').value;
var quadraticterm = document.getElementById('quad').value;
var uncertainty   = 4.74 * distance * (linearterm * distance + quadraticterm * distance * distance);
  // this log is just a nice bonus to track the math!
  console.log("DISTANCE: " + distance + " LINEAR: " + linearterm + " QUADRATIC: " + quadraticterm + " UNCERTAINTY: " + uncertainty + " END");
if (distance=="")
{
  uncertainty = 4.74 * distance * (linearterm * distance + quadraticterm * distance * distance);
}
else
{
  uncertainty = 4.74 * distance * (linearterm * distance + quadraticterm * distance * distance);
}
document.getElementById("uncertainty").innerHTML = Math.round(uncertainty * 100) / 100;
}
