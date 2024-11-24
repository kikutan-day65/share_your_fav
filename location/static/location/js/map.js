class MapManager {
    constructor(initLatitude, initLongitude, zoomLevel = 13) {
        this.map = L.map("map").setView(
            [initLatitude, initLongitude],
            zoomLevel
        );
        this.initializeMap();
        this.initializeSidebar();
    }

    initializeMap() {
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 18,
            attribution: "Map data &copy; OpenStreetMap contributors",
        }).addTo(this.map);
    }

    initializeSidebar() {
        this.sidebar = L.control
            .sidebar({ container: "sidebar" })
            .addTo(this.map);

        this.sidebar.on("content", (ev) => {
            switch (ev.id) {
                case "autopan":
                    this.sidebar.options.autopan = true;
                    break;
                default:
                    this.sidebar.options.autopan = false;
            }
        });
    }

    addMarkers() {
        let currentMarker = null;

        this.map.on("click", (e) => {
            const { lat, lng } = e.latlng;
            const greenIcon = new L.Icon({
                iconUrl:
                    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png",
                shadowUrl:
                    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41],
            });

            // 既存のマーカーがあれば削除
            if (currentMarker) {
                this.map.removeLayer(currentMarker);
            }

            // 新しいマーカーを追加
            currentMarker = L.marker([lat, lng], { icon: greenIcon }).addTo(
                this.map
            );

            // 通常のポップアップを作成
            const popupContent = `
                <b>Marker at:</b><br>
                Latitude: ${lat}<br>
                Longitude: ${lng}
            `;
            currentMarker.bindPopup(popupContent);

            // マーカーを追加した直後にポップアップを表示
            currentMarker.openPopup(); // これでポップアップを即座に表示

            // マーカークリック時にもポップアップを表示
            currentMarker.on("click", () => {
                currentMarker.openPopup();
            });
        });
    }

    showMarkers(locations) {
        for (let i = 0; i < locations.length; i++) {
            const location = locations[i];

            // マーカーを作成してマップに追加
            const marker = L.marker([
                location.fields.latitude,
                location.fields.longitude,
            ]).addTo(this.map);

            // 通常のポップアップを一度だけ設定
            const popupContent = `
                <b>${location.fields.name}</b><br>
                ${location.fields.description}
            `;
            marker.bindPopup(popupContent);

            // マーカークリック時にポップアップを表示
            marker.on("click", () => {
                // 通常のポップアップを表示
                marker.openPopup();
            });
        }
    }
}

export { MapManager };
