//
// map-location-view.js
// ====================
// Widok przystosowany do modelu `Location`, który wyświetla i zarządza poje-
// dynczym markerem na mapie. Dziedziczy z `MapObject`.
define(['jquery',
        'underscore',
        'backbone',
        'js/maps/map-object'],

function ($, _, Backbone, MapObjectView) {
    
    "use strict";
    
    var MapLocationView = MapObjectView.extend({
        
        getData: function () {
            
            var self = this,
                url = '/api-locations/locations/' + this.model.get('object_pk') + '/';
                                 
            $.get(url, function (m) {
                
                var contentString = window.locDialogTpl({
                        name: m.name,
                        img: m.image,
                        slug: m.slug
                    });
                    
                self.showInfo(contentString, self.map, self.marker);
            });
        }
    });
    
    return MapLocationView;
});