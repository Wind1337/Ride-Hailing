function UI(route)
{
    var map = new maplibregl.Map({
        container: 'ts-map-hero',
        style: 'https://api.maptiler.com/maps/streets/style.json?key=b74gkn1VskvsZy9K7x1q',
        center: [103.7597206, 1.3842917],
        zoom: 17
    });

    // start
    var origin = [103.7597206, 1.3842917];

    // end
    var destination = [103.7598897, 1.3848166];

    // A simple line from origin to destination.
    var route = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [
                        103.7597206,
                        1.3842917
                    ],
                    [
                        103.7598128,
                        1.384384
                    ],
                    [
                        103.7598587,
                        1.3844255
                    ],
                    [
                        103.7598896,
                        1.3844679
                    ],
                    [
                        103.7599179,
                        1.3845139
                    ],
                    [
                        103.7599453,
                        1.384573
                    ],
                    [
                        103.7599498,
                        1.3845918
                    ],
                    [
                        103.7599568,
                        1.3846207
                    ],
                    [
                        103.759955,
                        1.3846649
                    ],
                    [
                        103.759947,
                        1.3847091
                    ],
                    [
                        103.7599258,
                        1.3847559
                    ],
                    [
                        103.7598897,
                        1.3848166
                    ]
                ]
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
    var steps = 500;

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
                'line-width': 5,
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


function submitForm()
{
  document.getElementById('optionForm').submit();
}
