//
// map-object.js
// =============
// Prosty widok dla pojedynczego obiektu na mapie. Łączy widok Backbone z 
// obiektami google.maps. Przeznaczony do dalszego rozszerzenia przez klasy
// MapPointerView i MapLocationView.
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    var MapObjectView = Backbone.View.extend({
        
        initialize: function () {
            
            var self = this;
            var markerUrl = window.MAP_STATIC_URL + '/icons/marker-' + 
                    window.CONTENT_TYPES[self.model.get('content_type')].model;
                
                markerUrl += (window.devicePixelRatio > 1.5) ? '@2x.png' : '.png';
            
            var latLng = new google.maps.LatLng(
                this.model.get('latitude'),
                this.model.get('longitude')
            );
            
            this.marker = new google.maps.Marker({
                position: latLng,
                icon: markerUrl,
                content_type: self.model.get('content_type')
            });
            
            google.maps.event.addListener(this.marker, 'click', function () {
                self.getData();
            });
        },
        
        getData: function () {
            return true;
        },
        
        showInfo: function (contentString, map, marker) {
            var infoWindow = new google.maps.InfoWindow({
                    content: contentString
                });
            
            infoWindow.open(map, marker);
            
            $(document).one('click', function (e) {
                infoWindow.close();
            });
        }
    });
    
    return MapObjectView;
});