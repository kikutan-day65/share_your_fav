class LeafletMap {
    constructor(elementId, latitude, longitude, zoom, locationDataUrl) {
        this.elementId = elementId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.zoom = zoom;
        this.map = null;
        this.currentPin = null;
        this.baseUrl = locationDataUrl;
    }

    initializeMap(locationsData) {
        this.map = L.map(this.elementId, {
            center: [this.latitude, this.longitude],
            zoom: this.zoom,
        });

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "&copy; OpenStreetMap contributors",
        }).addTo(this.map);

        this.loadPinFromData(locationsData);

        this.dropPin();
    }

    loadPinFromData(locationsData) {
        locationsData.forEach((location) => {
            const marker = new L.marker([
                location.latitude,
                location.longitude,
            ]).addTo(this.map);

            marker.on("click", () => {
                console.log("marker is clicked!");

                const locationDataUrl = this.baseUrl.replace("0", location.id);

                //クリックしたらlocationの詳細を表示
                $.ajax({
                    url: locationDataUrl,
                    type: "GET",
                    dataType: "html",
                    success: (html) => {
                        this.showSidebar(html);
                    },
                    error: (xhr, status, error) => {
                        console.error("Error loading location data:", error);
                    },
                });
            });
        });
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

    showSidebar(html) {
        document.getElementById("mySidebar").style.width = "40%";
        document.getElementById("map").style.marginLeft = "40%";
        document.getElementById("map").style.width = "60%";

        document.getElementById("sidebarContent").innerHTML = html;
    }

    closeSidebar() {
        document.getElementById("mySidebar").style.width = "0";
        document.getElementById("map").style.marginLeft = "0";
        document.getElementById("map").style.width = "100%";
    }
}

export default LeafletMap;
