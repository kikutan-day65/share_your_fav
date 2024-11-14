class MapManager {
    constructor(mapContainerId, initLatitude, initLongitude, zoomLevel = 13) {
        this.map = L.map(mapContainerId).setView(
            [initLatitude, initLongitude],
            zoomLevel
        );
        this.currentMarker = null;
    }

    initializeMap() {
        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution:
                '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(this.map);
    }

    showMarkers(locations) {
        locations.forEach((location) => {
            L.marker([location.fields.latitude, location.fields.longitude])
                .addTo(this.map)
                .bindPopup(location.fields.name);
        });
    }

    addMarkers(locationUrls) {
        this.map.on("click", (event) => {
            const { lat, lng } = event.latlng;

            if (this.currentMarker) {
                this.map.removeLayer(this.currentMarker);
            }

            // 一時的にマーカをマップに落とす
            this.currentMarker = L.marker([lat, lng]).addTo(this.map);

            // ポップアップの内容作成
            let popupContent = `Latitude: ${lat}, Longitude: ${lng}`;

            if (locationUrls && locationUrls.location_create_form) {
                const createFormUrl = locationUrls.location_create_form;
                console.log(createFormUrl);
                popupContent += `<br><a href="/location/${createFormUrl}">Create New Location</a>`;
            }

            // ポップアップの表示
            this.currentMarker.bindPopup(popupContent).openPopup();
        });
    }
}

// Locationオブジェクトのためのクラス
class LocationManager {
    constructor(locationsData) {
        this.locations = JSON.parse(locationsData);
    }

    getLocations() {
        return this.locations;
    }
}

export { MapManager, LocationManager };
