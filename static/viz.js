var map;
function initMap() {
    map = new google.maps.Map(document.getElementById("map_canvas"), {
        center: {lat: 32.0833, lng: 34.8000},
        zoom: 8
    });

    var marker = new google.maps.Marker({
        position: {lat: 32.0833, lng: 34.8000},
        map: map,
        title: 'תל אביב'
    });
}