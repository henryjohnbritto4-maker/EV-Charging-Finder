document.addEventListener("DOMContentLoaded", function () {
    const mapDiv = document.getElementById("map");
    if (!mapDiv) return;

    const nearbyUrl = mapDiv.dataset.nearbyUrl;

    // Default center (fallback if geolocation is denied) - adjust to your city
    let map = L.map("map").setView([13.0827, 80.2707], 11);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
        maxZoom: 19
    }).addTo(map);

    let userMarker = null;
    const stationMarkers = [];

    function clearStationMarkers() {
        stationMarkers.forEach(m => map.removeLayer(m));
        stationMarkers.length = 0;
    }

    function loadNearbyStations(lat, lon) {
        fetch(`${nearbyUrl}?lat=${lat}&lon=${lon}`)
            .then(res => res.json())
            .then(data => {
                clearStationMarkers();

                if (!data.stations || data.stations.length === 0) {
                    console.log("No nearby stations found.");
                    return;
                }

                data.stations.forEach(station => {
                    const marker = L.marker([station.latitude, station.longitude])
                        .addTo(map)
                        .bindPopup(
                            `<strong>${station.name}</strong><br>
                             ${station.address}<br>
                             ${station.distance_km} km away<br>
                             Connector: ${station.connector_type}<br>
                             <a href="/stations/${station.id}">View Details</a>`
                        );
                    stationMarkers.push(marker);
                });
            })
            .catch(err => console.error("Error loading nearby stations:", err));
    }

    // Try to get the user's real location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                map.setView([lat, lon], 13);

                userMarker = L.marker([lat, lon], {
                    icon: L.divIcon({
                        className: "user-location-marker",
                        html: "📍",
                        iconSize: [24, 24]
                    })
                }).addTo(map).bindPopup("You are here").openPopup();

                loadNearbyStations(lat, lon);
            },
            function () {
                console.log("Location access denied. Showing default map view.");
            }
        );
    }
});