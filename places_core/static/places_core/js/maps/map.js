//
// map.js
// ======
// Główny widok mapy.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/maps/map-collection',
        'js/maps/map-location-view',
        'js/maps/map-pointer-view',
        'js/maps/markerclusterer'],

function ($, _, Backbone, MapCollection, MapLocationView, MapPointerView) {
    
    "use strict";
    
    var CivilMap = Backbone.View.extend({
        
        el: '#map',
        
        cluster: null,
        
        initialize: function (map, markers) {
            this.map = map;
            this.markers = [];
            this.collection = new MapCollection(markers);
            this.render();
        },
        
        // Metoda dodaje marker na podstawie pola `content_type` modelu odpowia-
        // dającego ID danego typu zawartości. Markery podzielone są na dwie
        // główne grupy: lokacje oraz pozostałe. Tutaj wywołujemy odpowiedni
        // konstruktor.
        addMarker: function (item) {
            
            var viewClassName;
            
            if (window.CONTENT_TYPES[item.get('content_type')].model === 'location') {
                viewClassName = MapLocationView;
            } else {
                viewClassName = MapPointerView;
            }
            
            var markerView = new viewClassName({
                model: item
            });
            
            markerView.map = this.map;
            this.markers.push(markerView.marker);
        },
        
        // FIXME: refreshMarkers i render oryginalnie miały zapobiec powtarzaniu
        // kodu przy filtrowaniu markerów. W tym momencie metoda `filter` w 
        // ogóle z nich nie korzysta.
        refreshMarkers: function () {
            this.collection.each(function (item) {
                this.addMarker(item);
            }, this);
        },
        
        // FIXME: j/w
        render: function () {
            
            if (!_.isNull(this.cluster)) {
                this.cluster.clearMarkers();
            }
            
            this.refreshMarkers();
            
            console.log(this.markers.length);
            var i = 0;
            _.each(this.markers, function (m) {
                console.log(m.content_type);
                i++
            }, this);
            console.log(i);
            
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
        
        // Metoda filtrująca markery w kolekcji.
        filter: function (filters) {
            
            var mlist = [];
            
            _.each(filters, function (filter) {
                filter = parseInt(filter, 10);
                mlist = mlist.concat(_.where(this.markers, 
                        {content_type:filter}));
            }, this);
            
            if (!_.isNull(this.cluster)) {
                this.cluster.clearMarkers();
            }
            
            this.cluster = new MarkerClusterer(this.map, mlist, {
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