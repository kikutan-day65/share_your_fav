import LeafletMap from "./map.js";

const locationsData = JSON.parse(
    document.getElementById("locations-data").textContent
);

const locationDataUrl = JSON.parse(
    document.getElementById("data-url").textContent
);

var mapInstance = new LeafletMap("map", 35.4437, 139.638, 13, locationDataUrl);
mapInstance.initializeMap(locationsData);

// Call the closeSidebar function when x button is clicked in the sidebar
document.getElementById("closeSidebarButton").addEventListener("click", () => {
    mapInstance.closeSidebar();
});
