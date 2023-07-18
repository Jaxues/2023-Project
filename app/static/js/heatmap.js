// Retrieve the heatmap data element
var heatmapDataElement = document.getElementById('heatmap-data');

// Get the text content of the element
var heatmapData = heatmapDataElement.textContent;

console.log('heatmapData:', heatmapData); // Log the value of heatmapData to the console

// Parse the JSON data as a JavaScript object
var parsedData = JSON.parse(heatmapData);

// Get Success Color for Heatmap
var successColor = getComputedStyle(document.documentElement).getPropertyValue('--success-color');
console.log('successColor',successColor)
// Get Other color for heatmap
var primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color');
console.log('primaryColor',primaryColor)
// Set up the dimensions for the heatmap
var cellSize = 30; // Set the desired size of each cell
var margin = { top: 20, right: 20, bottom: 20, left: 20 };
var width = Object.keys(parsedData).length * cellSize + margin.left + margin.right;
var height = cellSize + margin.top + margin.bottom;

// Create the canvas for the heatmap
var canvas = document.createElement('canvas');
canvas.width = width;
canvas.height = height;

// Get the 2D context of the canvas
var context = canvas.getContext('2d');

// Create a color scale based on the number of habits completed
var colorScale = d3.scaleLinear()
  .domain([0, d3.max(Object.values(parsedData))])
  .range([primaryColor, successColor]);

// Draw the heatmap cells
Object.entries(parsedData).forEach(function (d, i) {
  var x = i * cellSize;
  var y = 0;
  var value = d[1];
  
  context.fillStyle = colorScale(value);
  context.fillRect(x, y, cellSize, cellSize);
});

// Append the canvas to the heatmap container
var heatmapContainer = document.getElementById('myheatMap');
heatmapContainer.appendChild(canvas);

// Add event listener to show the number of habits completed on hover
canvas.addEventListener('mousemove', function (event) {
  var rect = canvas.getBoundingClientRect();
  var x = event.clientX - rect.left;
  var y = event.clientY - rect.top;
  var column = Math.floor(x / cellSize);
  var value = parsedData[Object.keys(parsedData)[column]];
  
  canvas.title = 'Habits Completed: ' + value;
});

// Clear the tooltip on mouseout
canvas.addEventListener('mouseout', function () {
  canvas.title = '';
});
console.log('pasedData',parsedData)
