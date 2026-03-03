// onboarding_map.js
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('location-search');
    const openMapBtn = document.getElementById('open-map-btn');
    const mapPopup = document.getElementById('locationPopup');
    const closeMapBtn = document.getElementById('close-map-btn');
    const confirmBtn = document.getElementById('confirm-location-btn');

    let map, marker;

    const initMap = () => {
        if (map) return;
        map = L.map('map-container').setView([20.5937, 78.9629], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        map.on('click', (e) => {
            if (marker) map.removeLayer(marker);
            marker = L.marker(e.latlng).addTo(map);
        });
    };

    if (openMapBtn) {
        openMapBtn.addEventListener('click', () => {
            mapPopup.style.display = 'flex';
            setTimeout(initMap, 100);
        });
    }

    if (closeMapBtn) closeMapBtn.addEventListener('click', () => mapPopup.style.display = 'none');

    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            if (marker) {
                const lat = marker.getLatLng().lat;
                const lng = marker.getLatLng().lng;
                document.getElementById('id_lat').value = lat;
                document.getElementById('id_lng').value = lng;
                mapPopup.style.display = 'none';
                searchInput.value = `Selected: ${lat.toFixed(4)}, ${lng.toFixed(4)}`;
            }
        });
    }
});
