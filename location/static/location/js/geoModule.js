class MapManager {
    constructor(mapContainerId, initLatitude, initLongitude, zoomLevel = 13) {
        this.map = L.map(mapContainerId).setView(
            [initLatitude, initLongitude],
            zoomLevel
        );
    }

    initializeMap() {
        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution:
                '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(this.map);
    }

    addMarkers(locations) {
        locations.forEach((location) => {
            L.marker([location.fields.latitude, location.fields.longitude])
                .addTo(this.map)
                .bindPopup(location.fields.name);
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
