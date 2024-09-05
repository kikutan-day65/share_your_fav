class LeafletMap {
    constructor(elementId, latitude, longitude, zoom) {
        this.elementId = elementId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.zoom = zoom;
    };

    initializeMap() {
        var map = L.map(this.elementId, {
            center: [this.latitude, this.longitude],
            zoom: this.zoom
        });

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
    };
};

var mapInstance = new LeafletMap("map", 35.4437, 139.6380, 13);
intialMap = mapInstance.initializeMap();
