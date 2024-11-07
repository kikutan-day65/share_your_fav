import { MapManager, LocationManager } from "./geoModule.js";

const mapController = new MapManager("map", 35.466, 139.6221, 13);
mapController.initializeMap();

// locations-dataスクリプトタグからデータを取得
const locationsDataString = JSON.parse(
    document.getElementById("locations-data").textContent
);

const locationsData = JSON.parse(locationsDataString);

// ループして.nameにアクセスする例
locationsData.forEach((location) => {
    console.log(location.fields.name); // nameを出力
});

// const locationsObj = new LocationManager(locationsData);
