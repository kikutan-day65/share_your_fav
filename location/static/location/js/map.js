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

            this.showSidebar(e.latlng.lat, e.latlng.lng);
            this.map.invalidateSize();

            // The zoom level can be set using the 2nd argument
            this.map.setView([e.latlng.lat, e.latlng.lng]);
        });
    }

    showSidebar(latitude, longitude) {
        document.getElementById("mySidebar").style.width = "40%";
        document.getElementById("map").style.marginLeft = "40%";
        document.getElementById("map").style.width = "60%";

        fetch("location-form/")
            .then((response) => response.text())
            .then((html) => {
                document.getElementById("sidebarContent").innerHTML = html;

                console.log(document.getElementById("id_latitude")); // 要素が表示されるか確認
                console.log(document.getElementById("id_longitude")); // 要素が表示されるか確認

                document.getElementById("id_latitude").value = latitude;
                document.getElementById("id_longitude").value = longitude;
                g;
            })
            .catch((error) => {
                console.log("Error loading the form:", error);
            });
    }
}

export default LeafletMap;
