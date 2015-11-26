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
        $.each(data.markers, function(index, city) {
            var marker = new google.maps.Marker({
                position: {lat: city.lat, lng: city.lng},
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    strokeColor: "#FFFFFF",
                    strokeWeight: 1,
                    fillColor: "rgb(255, " + city.color + ", 0)",
                    fillOpacity: 1,
                    scale: city.size
                },
                map: map,
                title: city.title
            });
            marker.addListener("click", function() {
                showDetails(city);
                showInvolved(city);
                compared_city = {id: 5000, title: "תל אביב -יפו"}
                showComparison(city, compared_city);
            });
        });
    });
}

function showDetails(city) {
    $("#details").show();
    $("#total-accidents").text(city.total);
    $("#city-name").text(city.title);
    $("#light-accidents").text(city.light);
    $("#severe-accidents").text(city.severe);
    drawCircle("chart-light", city.light_size);
    drawCircle("chart-severe", city.severe_size);

    $("html, body").animate({
        scrollTop: $("#details").offset().top
    }, 2000);
}

function drawCircle(id, size) {
    $("#" + id).css("width", size);
    $("#" + id).css("height", size);
    $("#" + id).css("border-radius", size/2);
}

function showInvolved(city) {
    $("#involved").show();
    $("#involved-num").text(city.involved_count);
    $("#young-num").text(city.young_count);
    $("#middle-num").text(city.middle_count);
    $("#old-num").text(city.old_count);
}

function showComparison(city, compared_city) {
    $("#timeline-comparison").show();
    $("#city-name1").text(city.title);
    $("#city-name2").text(compared_city.title);
    $("#timeline-plot").attr("src",
        "timeline.png?city1=" + city.id + "&city2=" + compared_city.id);
}