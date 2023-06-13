// Retrieve the heatmap data element
var heatmapDataElement = document.getElementById('heatmap-data');

// Get the text content of the element
var heatmapData = heatmapDataElement.textContent;


console.log('heatmapData:', heatmapData); // Log the value of heatmapData to the console

// Parse the JSON data as a JavaScript object
var parsedData = JSON.parse(heatmapData);

console.log('Parsed Data:', parsedData); // Log the parsed data to the console