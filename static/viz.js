var map;
function initMap() {
    map = new google.maps.Map(document.getElementById("map_canvas"), {
        center: {lat: 32.0833, lng: 34.8000},
        zoom: 8
    });

    fetchMarkers();
}

function fetchMarkers() {
    $.getJSON("/markers", function(data) {
        $.each(data.markers, function(index, value) {
            var marker = new google.maps.Marker({
                position: {lat: value.lat, lng: value.lng},
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    strokeColor: "#FFFFFF",
                    strokeWeight: 1,
                    fillColor: "rgb(255, " + value.color + ", 0)",
                    fillOpacity: 1,
                    scale: value.size
                },
                map: map,
                title: value.title
            });
        });
    });
}