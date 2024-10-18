class MapManager {
    constructor(mapContainerId, initLatitude, initLongitude, zoomLevel = 13) {
        this.map = L.map(mapContainerId).setView(
            [initLatitude, initLongitude],
            zoomLevel
        );
    }

    InitializeMap() {
        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution:
                '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(this.map);
    }
}

// // Locationオブジェクトのためのクラス
// class LocationManager {
//     constructor(latitude, longitude) {}
// }
