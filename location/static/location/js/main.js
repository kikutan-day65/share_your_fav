import { MapManager } from "./map.js";

const mapController = new MapManager(35.466, 139.6221, 13);

// locations-dataスクリプトタグからlocationデータを取得
const locationsDataString = JSON.parse(
    document.getElementById("locations-data").textContent
);

// 全URLを取得
const locationUrls = JSON.parse(
    document.getElementById("location-urls").textContent
);
const locationsData = JSON.parse(locationsDataString);
mapController.showMarkers(locationsData);

mapController.addMarkers(locationUrls);
