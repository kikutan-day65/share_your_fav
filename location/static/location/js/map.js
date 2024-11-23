import createCustomPopupControl from "./map-popup.js";
const { CustomPopup, custompopup } = createCustomPopupControl();

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

            // 既存のマーカーを削除
            if (currentMarker) {
                this.map.removeLayer(currentMarker);
            }

            // 新しいマーカーを追加
            currentMarker = new L.marker([lat, lng]).addTo(this.map);

            // カスタムポップアップを作成する関数
            const showPopup = () => {
                // 既存のカスタムポップアップを削除
                if (this.customPopup) {
                    this.customPopup.removeFrom(this.map);
                    this.customPopup = null; // ポップアップ参照をクリア
                }

                // ポップアップ用のHTML要素を生成または再利用
                const placeholderId = `popup-${Date.now()}`; // 固有IDを生成
                let placeholder = document.getElementById(placeholderId);
                if (!placeholder) {
                    placeholder = document.createElement("div");
                    placeholder.id = placeholderId;
                    document.body.appendChild(placeholder);
                }

                // 新しいカスタムポップアップを作成
                this.customPopup = custompopup(placeholderId, {
                    closeButton: true,
                    position: "left",
                    autoPan: true,
                });

                // ポップアップが閉じられた際の処理を追加
                this.customPopup.on("close", () => {
                    this.customPopup = null; // ポップアップ参照をクリア
                });

                // ポップアップに内容を設定
                this.customPopup.setContent(`
                    <b>Marker at:</b><br>
                    Latitude: ${lat}<br>
                    Longitude: ${lng}
                `);

                // マップにポップアップを追加して表示
                this.customPopup.addTo(this.map);
                this.customPopup.show();
            };

            // マーカー追加直後にポップアップを表示
            showPopup();

            // マーカークリック時にもポップアップを表示
            currentMarker.on("click", () => {
                if (!this.customPopup) {
                    showPopup();
                } else {
                    this.customPopup.show();
                }
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

            // マーカークリック時にカスタムポップアップを作成
            marker.on("click", () => {
                // 既存のポップアップを削除する場合
                if (this.customPopup) {
                    this.customPopup.removeFrom(this.map);
                }

                // 新しい`placeholder`を動的に作成
                const placeholderId = `popup-${i}`;
                let placeholder = document.getElementById(placeholderId);
                if (!placeholder) {
                    placeholder = document.createElement("div");
                    placeholder.id = placeholderId;
                    document.body.appendChild(placeholder);
                }

                // 新しいポップアップを作成
                this.customPopup = custompopup(placeholderId, {
                    closeButton: true,
                    position: "left",
                    autoPan: true,
                });

                // ポップアップに内容を設定
                this.customPopup.setContent(`
                    <b>${location.fields.name}</b><br>
                    ${location.fields.description}
                `);

                // ポップアップをマップに追加して表示
                this.customPopup.addTo(this.map);
                this.customPopup.show();
            });
        }
    }
}

export { MapManager };
