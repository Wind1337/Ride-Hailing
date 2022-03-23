/*function routing(node, trip)
{
    var map = L.map('ts-map-hero').setView([node[0][0], node[0][1]], 15);
    L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=b74gkn1VskvsZy9K7x1q',
    {
        tileSize: 512,
        zoomOffset: -1,
        minZoom: 1,
        attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
        crossOrigin: true
    }).addTo(map);

    var polyline = L.polyline(node).addTo(map);
    polyline.setStyle({
        color: 'red',
        weight: 5
    });

    var passPickupMarker = L.marker([node[index][0], node[index][1]]).addTo(map);
    var passDropOffMarker = L.marker([node[node.length-1][0], node[node.length-1][1]]).addTo(map);

    passPickupMarker.bindPopup("Pick Up Point");
    passDropOffMarker.bindPopup("Drop Off Point")
}*/

var map = L.map('ts-map-hero').setView([1.3790334, 103.7642649], 17);
L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=b74gkn1VskvsZy9K7x1q',{
tileSize: 512,
zoomOffset: -1,
minZoom: 1,
attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
crossOrigin: true
}).addTo(map);

console.log("test");

var passPickupMarker = L.marker([1.3790334, 103.7642649]).addTo(map);
var passDropOffMarker = L.marker([1.3790293, 103.7640756]).addTo(map);
var driLocation = L.marker([1.3842443, 103.7598278]).addTo(map);


function submitForm()
{
  document.getElementById('optionForm').submit();
}