class LeafletMap {
    constructor(elementId, latitude, longitude, zoom) {
        this.elementId = elementId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.zoom = zoom;
        this.map = null;
        this.currentPin = null;
    }

    initializeMap() {
        this.map = L.map(this.elementId, {
            center: [this.latitude, this.longitude],
            zoom: this.zoom,
        });

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "&copy; OpenStreetMap contributors",
        }).addTo(this.map);

        this.dropPin();
    }

    dropPin() {
        this.map.on("click", (e) => {
            if (this.currentPin) {
                this.map.removeLayer(this.currentPin);
            }

            this.currentPin = new L.marker([e.latlng.lat, e.latlng.lng]).addTo(
                this.map
            );

            this.showSidebar();
            this.map.invalidateSize();

            // The zoom level can be set using the 2nd argument
            this.map.setView([e.latlng.lat, e.latlng.lng]);
        });
    }

    showSidebar() {
        document.getElementById("mySidebar").style.width = "30%";
        document.getElementById("map").style.marginLeft = "30%";
        document.getElementById("map").style.width = "70%";
    }
}

var mapInstance = new LeafletMap("map", 35.4437, 139.638, 13);
mapInstance.initializeMap();
