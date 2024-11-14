import { MapManager, LocationManager } from "./geoModule.js";

const mapController = new MapManager("map", 35.466, 139.6221, 13);
mapController.initializeMap();

// locations-dataスクリプトタグからデータを取得
const locationsDataString = JSON.parse(
    document.getElementById("locations-data").textContent
);
const locationManager = new LocationManager(locationsDataString);

// 全URLを取得
const locationUrls = JSON.parse(
    document.getElementById("location-urls").textContent
);
// console.log(locationUrls);

mapController.showMarkers(locationManager.getLocations());

mapController.addMarkers(locationUrls);
