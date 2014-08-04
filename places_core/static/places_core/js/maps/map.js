//
// map.js
// ======
// Główny widok mapy.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/maps/map-collection',
        'js/maps/map-object',
        'js/maps/markerclusterer'],

function ($, _, Backbone, MapCollection, MapObject) {
    
    "use strict";
    
    var CivilMap = Backbone.View.extend({
        
        el: '#map',
        
        initialize: function (map, markers) {
            this.map = map;
            this.markers = [];
            this.collection = new MapCollection(markers);
            
            this.collection.each(function (item) {
                var markerView = new MapObject({
                    model: item
                });
                markerView.map = this.map;
                this.markers.push(markerView.marker);
            }, this);
            
            this.cluster = new MarkerClusterer(this.map, this.markers, {
                maxZoom: 10,
                gridSize: 30,
                styles: [{
                    url: window.STATIC_URL + '/images/people35.png',
                    height: 35,
                    width: 35,
                    anchor: [16, 0],
                    textColor: '#ff00ff',
                    textSize: 10
                }]
            });
        },
        
        filter: function (filters) {
            this.cluster.clearMarkers();
            
            this.cluster = new MarkerClusterer(this.map, this.markers, {
                maxZoom: 10,
                gridSize: 30,
                styles: [{
                    url: window.STATIC_URL + '/images/people35.png',
                    height: 35,
                    width: 35,
                    anchor: [16, 0],
                    textColor: '#ff00ff',
                    textSize: 10
                }]
            });
        }
    });
    
    return CivilMap;
});