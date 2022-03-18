function plotting(route)
{
    /*var map = L.map('mapdiv').setView([route[0][0], route[0][1]], 17);
    L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=b74gkn1VskvsZy9K7x1q',
    {
        tileSize: 512,
        zoomOffset: -1,
        minZoom: 1,
        attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
        crossOrigin: true
    }).addTo(map);*/

    /*route.forEach(coordinate => {
      console.log(coordinate[0])
      console.log(coordinate[1])
    })*/

    /* var passPickupMarker = L.marker([1.3790334, 103.7642649]).addTo(map);
    var passDropOffMarker = L.marker([1.3790293, 103.7640756]).addTo(map);
    var driLocation = L.marker([1.3842443, 103.7598278]).addTo(map);

    var distanceFromLocationToPickup = L.polygon([[1.3842443, 103.7598278], [1.3790334, 103.7642649]]).addTo(map);

    var distanceFromPickupToDropOff = L.polygon([[1.3790334, 103.7642649], [1.3790293, 103.7640756]]).addTo(map);

    passPickupMarker.bindPopup("Pick Up Point").openPopup();
    passDropOffMarker.bindPopup("Drop Off Point")
    driLocation.bindPopup("Driver's Location")
    distanceFromLocationToPickup.bindPopup("Distance from Driver's Location to Pick-Up Venue")
    distanceFromPickupToDropOff.bindPopup("Distance from Pick-Up Venue to Drop-Off Venue") */

    var map = L.map('mapdiv').setView([1.3793232, 103.7725659], 17);
    L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=b74gkn1VskvsZy9K7x1q',
    {
    tileSize: 512,
    zoomOffset: -1,
    minZoom: 1,
    attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
    crossOrigin: true
    }).addTo(map);

    var polyline = L.polyline(route).addTo(map);

    var displayPass = function ()
    {
      $("#passenger-form").modal("show");
    };
    var formPass = document.getElementById("pass-form");
    formPass.addEventListener("submit", onSubmitForm);

    var displayDri = function ()
    {
      $("#driver-form").modal("show");
    };
    var formDri = document.getElementById("dri-form");
    formDri.addEventListener("submit", onSubmitForm);

    var submitted = function onSubmitForm(e)
    {
      e.preventDefault();
      $("#passenger-form")[0].reset();
      $("#passenger-form").modal("hide");
      $("#driver-form")[0].reset();
      $("#driver-form").modal("hide");
    }

    function submitForm()
    {
      document.getElementById('optionForm').submit();
    }
}
