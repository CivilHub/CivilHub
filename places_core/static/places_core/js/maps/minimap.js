//
// minimap.js
// ==========
// Display minimap for different content types.
define(['jquery',
        'bootbox',
        'async!//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false'],

function ($, bootbox) {
    
    "use strict";
    
    $.fn.minimap = function (markers) {
        return $(this).each(function () {
            var $this = $(this),
                center = markers[0] || {lat: 0, lng: 0},
                el = document.getElementById($this.attr('id')),
                mapOptions = {
                    zoom: 6,
                    center: new google.maps.LatLng(
                        parseInt(center.lat, 10),
                        parseInt(center.lng, 10)),
                    width: 300,
                    height: 300
                },
                map = new google.maps.Map(el, mapOptions);
                
            $(markers).each(function () {
                var marker = this,
                    m = new google.maps.Marker(),
                    pos = new google.maps.LatLng(
                        parseInt(this.lat, 10), parseInt(this.lng, 10)
                    );
                    
                m.setMap(map);
                m.setPosition(pos);
                
                google.maps.event.addListener(m, 'click', function() {
                    bootbox.confirm(gettext("Are you sure you want to delete this marker?"), function (resp) {
                        if (resp) {
                            $.ajax({
                                beforeSend: function (xhr, settings) {
                                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                                },
                                type: 'POST',
                                url: '/maps/remove/',
                                data: {pk: marker.pk},
                                dataType: 'json',
                                success: function (resp) {
                                    window.message.success(resp.message);
                                    m.setVisible(false);
                                },
                                error: function (err) {
                                    console.log(err);
                                }
                            });
                        }
                    });
                });
            });
        });
    };
});