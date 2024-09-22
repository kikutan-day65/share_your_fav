import LeafletMap from "./map.js";


var mapInstance = new LeafletMap("map", 35.4437, 139.638, 13);
mapInstance.initializeMap();

function closeSidebar() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("map").style.marginLeft = "0";
    document.getElementById("map").style.width = "100%";
}

document.addEventListener("DOMContentLoaded", function () {
    // location-dataのJSONを取得してパース
    const locationData = JSON.parse(
        document.getElementById("locations-data").textContent
    );

    // パースしたデータをコンソールに表示
    console.log(locationData);

    // 各locationにアクセス (例: 最初のlocationのname)
    locationData.forEach((location) => {
        console.log(location.name); // 各locationのname
        console.log(location.latitude); // 各locationのlatitude
        console.log(location.longitude); // 各locationのlongitude
    });
});
