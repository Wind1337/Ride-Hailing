function UI(route_path, marker)
{
    if (passenger_1 == "None")
    {
        document.getElementById("traffic").disabled = true;
    }

    var map = new maplibregl.Map({
        container: 'ts-map-hero',
        style: 'https://api.maptiler.com/maps/streets/style.json?key=b74gkn1VskvsZy9K7x1q',
        center: [route_path[0][0], route_path[0][1]],
        zoom: 15
    });

    // start
    var origin = [route_path[0][0], route_path[0][1]];

    // end
    var destination = [route_path[route_path.length - 1][0], route_path[route_path.length - 1][1]];


    for(let counter = 0; counter < marker.length; counter++)
    {
        if (counter == 0) {         // [0] is first passenger's pickup
            var pickup_marker = new maplibregl.Marker({color: "#FB9F2C"}).setLngLat(marker[counter])
            .setPopup(new maplibregl.Popup().setHTML(passenger_1 + "'s Pickup")).addTo(map);
        }
        else if (counter == 1) {    // [1] is first passenger's dropoff
            var pickup_marker = new maplibregl.Marker({color: "#B191EB"}).setLngLat(marker[counter])
            .setPopup(new maplibregl.Popup().setHTML(passenger_1+"'s Dropoff")).addTo(map);
        }
        else if (counter == 2) {    // [2] is second passenger's pickup
            var pickup_marker = new maplibregl.Marker({color: "#FB9F2C"}).setLngLat(marker[counter])
            .setPopup(new maplibregl.Popup().setHTML(passenger_2 + "'s Pickup")).addTo(map);
        }
        else {                      // [3] is second passenger's dropoff
            var pickup_marker = new maplibregl.Marker({color: "#B191EB"}) .setLngLat(marker[counter])
            .setPopup(new maplibregl.Popup().setHTML(passenger_2 + "'s Dropoff")).addTo(map);
        }
    }



    // A simple line from origin to destination.
    var route = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': route_path
            }
        }]
    };

    // A single point that animates along the route.
    // Coordinates are initially set to origin.
    var point = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Point',
                'coordinates': origin
            }
        }]
    };

    // Calculate the distance in kilometers between route start/end point.
    var lineDistance = turf.lineDistance(route.features[0], 'kilometers');

    var arc = [];

    // Number of steps to use in the arc and animation, more steps means
    // a smoother arc and animation, but too many steps will result in a
    // low frame rate
    var steps = 1000;

    // Draw an arc between the `origin` & `destination` of the two points
    for (var i = 0; i < lineDistance; i += lineDistance / steps) {
    var segment = turf.along(route.features[0], i, 'kilometers');
    arc.push(segment.geometry.coordinates);
    }

    // Update the route with calculated arc coordinates
    route.features[0].geometry.coordinates = arc;

    // Used to increment the value of the point measurement against the route.
    var counter = 0;

    map.on('load', function () {
        // Add a source and layer displaying a point which will be animated in a circle.
        map.addSource('route', {
            'type': 'geojson',
            'data': route
        });

        map.addSource('point', {
            'type': 'geojson',
            'data': point
        });

        map.addLayer({
            'id': 'route',
            'source': 'route',
            'type': 'line',
            'paint': {
                'line-width': 4,
                'line-color': '#FF0000'
            }
        });

        map.addLayer({
            'id': 'point',
            'source': 'point',
            'type': 'symbol',
            'layout': {
                'icon-image': 'car_15',
                'icon-rotate': ['get', 'bearing'],
                'icon-rotation-alignment': 'map',
                'icon-overlap': 'always',
                'icon-ignore-placement': true
            }
        });

        function animate() {
            // Update point geometry to a new position based on counter denoting
            // the index to access the arc.
            point.features[0].geometry.coordinates = route.features[0].geometry.coordinates[counter];

            // Calculate the bearing to ensure the icon is rotated to match the route arc
            // The bearing is calculate between the current point and the next point, except
            // at the end of the arc use the previous point and the current point
            point.features[0].properties.bearing = turf.bearing(
            turf.point(route.features[0].geometry.coordinates[counter >= steps ? counter - 1 : counter]),
            turf.point(route.features[0].geometry.coordinates[counter >= steps ? counter : counter + 1]));

            // Update the source with this new data.
            map.getSource('point').setData(point);

            // Request the next frame of animation so long the end has not been reached.
            if (counter < steps) {
                requestAnimationFrame(animate);
            }

            counter = counter + 1;

        }

        // Start the animation.
        animate(counter);
    });
}


/*var map = L.map('ts-map-hero').setView([1.3790334, 103.7642649], 17);
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
var driLocation = L.marker([1.3842443, 103.7598278]).addTo(map);*/

document.body.innerHTML = document.body.innerHTML.replace(/AND/g, '<br><br>')

function submitForm()
{
  document.getElementById('optionForm').submit();
}
