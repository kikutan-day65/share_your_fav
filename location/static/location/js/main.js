import LeafletMap from "./map.js";

const locationsData = JSON.parse(
    document.getElementById("locations-data").textContent
);

// console.log(locationsData);

var mapInstance = new LeafletMap("map", 35.4437, 139.638, 13);
mapInstance.initializeMap(locationsData);

// Call the closeSidebar function when x button is clicked in the sidebar
document.getElementById("closeSidebarButton").addEventListener("click", () => {
    mapInstance.closeSidebar();
});
