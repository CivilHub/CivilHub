//
// map.js
// ======
//
// Główny obiekt obsługujący mapę.

define(['jquery',
        'underscore',
        'leaflet'],

function ($, _, L) {
    
    "use strict";
    
    var icons = {}; // Ikony pobieramy ze skryptu w templatce
    
    var defaults = {
        // ID DOM elementu dla mapy
        elementID: 'map',
        // Base url to get marker data
        apiURL: '/api-maps/data/',
        // URL to fetch info about specific object
        infoURL: '/api-maps/objects/',
        // URL dla map tails
        mapTailURL: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        // Minimalne zbliżenie, przy jakim pokazujemy pojedyncze markery:
        minZoom: 10,
        // Maksymalne możliwe zbliżenie - ze względu na openmaps
        maxZoom: 18,
        // Początkowe opcje mapy
        startZoom: 10,
        center: [0, 0],
        attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
    };
    
    // Main map constructor
    //
    // @param options { object } Simple object with options. See options for details.
    
    var Map = function (options) {
        // Array to hold marker so we have some hooks to manipulate them
        this.markers = [];
        // Array to hold cluster markers
        this.clusters = [];
        // Array of content types to fetch with every API request
        this.filters = [];
        // Fetch only data related to this location
        this.location = null;
        this.opts = $.extend(defaults, options);
        this.initialize();
        this.map.on('zoomend dragend', function () {
            this.fetchData();
        }.bind(this));
        this.map.on('zoomend', function () {
            this.clearClusters();
            // Hide or show control panel - show it only when single
            // markers are visible.
            if (this.map.getZoom() >= this.opts.minZoom) {                
                $('#map-options-toggle').fadeIn('fast');
                $('#map-options-panel').fadeIn('fast');
            } else {
                $('#map-options-toggle').fadeOut('fast');
                $('#map-options-panel').fadeOut('fast');
            }
        }.bind(this));
        // Fetch starting point if zoom is big enough
        if (this.map.getZoom() >= this.opts.minZoom) {
            this.fetchData();
        }
    };
    
    // Init map and create icon objects.
    
    Map.prototype.initialize = function () {
        var center = this.opts.center;
        // Mark active marker when 'show on map' option is used
        if (!_.isUndefined(CIVILAPP.current)) {
            var m = CIVILAPP.current;
            center = [m.latitude, m.longitude];
            this.activeMarker = L.marker(center);
        }
        this.map = L.map(this.opts.elementID)
                    .setView(center, this.opts.startZoom);
        L.tileLayer(this.opts.mapTailURL, {
            attribution: this.opts.attribution,
            maxZoom: this.opts.maxZoom
        }).addTo(this.map);
        // Create icons for different marker types
        _.each(CIVILAPP.icons, function (icon, key) {
            icons[key] = L.icon(icon);
        });
    };
    
    // Get markers from server
    
    Map.prototype.fetchData = function () {
        var mapData = {
            zoom: this.map.getZoom(),
            lat: this.map.getCenter().lat,
            lng: this.map.getCenter().lng
        };
        // Check for content type filters
        if (!_.isEmpty(this.filters)) {
            mapData.filters = this.filters.join(',');
        }
        // Check for location filters
        if (!_.isNull(this.location)) {
            mapData.location = this.location;
        }
        // Clear markers on zoom-out
        if (mapData.zoom < this.opts.minZoom) {
            this.clearMarkers();
            //return false;
        } else {
            this.clearClusters();
        }
        $.get(this.opts.apiURL, mapData, function (response) {
            this.updateMarkers(response);
        }.bind(this));
    };
    
    // Process server data and create new markers/delete old
    //
    // @param markers { array } Array with markers fetched from server
    
    Map.prototype.updateMarkers = function (markers) {
        var indexes = [];
        // Create new markers
        _.each(markers, function (item, idx) {
            if (this.map.getZoom() >= this.opts.minZoom) {
                this.addMarker(item);
            } else {
                this.addCluster(item);
            }
        }, this);
        // Find markers that are no longer available
        _.each(this.markers, function (marker) {
            var chk = _.find(markers, function (m) {
                var latlng = marker.getLatLng();
                return latlng.lat === m.latitude && latlng.lng === m.longitude;
            }, this);
            if (_.isUndefined(chk)) {
                indexes.push(marker);
            }
        }, this);
        // Delete unwanted old markers
        _.each(indexes, function (marker) {
            this.map.removeLayer(marker);
            this.markers.splice(this.markers.indexOf(marker), 1);
        }, this);
    };
    
    // Place new cluster on map
    //
    // @param item { object } Cluster object fetched from server
    
    Map.prototype.addCluster = function (item) {
        var cluster = L.marker([item.lat, item.lng], {
            icon: L.divIcon({
                className: 'count-icon',
                html: item.counter,
                iconSize: [40, 40]
            })
        });
        var latlng = L.latLng(item.lat, item.lng);
        
        // Check if cluster already exists
        var chk = _.find(this.clusters, function (cluster) {
            return cluster.getLatLng().equals(latlng);
        });
        if (!_.isUndefined(chk)) return false;
        
        this.map.addLayer(cluster);
        this.clusters.push(cluster);
        
        cluster.on('click', function () {
            this.map.setView(cluster.getLatLng(), 10);
        }.bind(this));
    };
    
    // Destroy entire clusters array
    
    Map.prototype.clearClusters = function () {
        _.each(this.clusters, function (cluster) {
            this.map.removeLayer(cluster);
        }, this);
        this.clusters = [];
    };
    
    // Place new marker on map
    //
    // @param item { object } Marker object fetched from server
    
    Map.prototype.addMarker = function (item) {
        var marker = L.marker([item.latitude, item.longitude], {
            icon: icons[item.content_type]
        });
        var latlng = L.latLng(item.latitude, item.longitude);
        
        // Check if marker already exists
        var chk = _.find(this.markers, function (marker) {
            return marker.getLatLng().equals(latlng);
        });
        if (!_.isUndefined(chk)) return false;
        
        // Extra metadata to communicate with server
        _.extend(marker, {meta:{ct:item.content_type,pk:item.object_pk}});
        
        this.map.addLayer(marker);
        this.markers.push(marker);
        
        // Check if marker is selected when option 'show on map' is used, but
        // only first time after map is loaded.
        if (!_.isUndefined(this.activeMarker)) {
            if (marker.getLatLng().equals(this.activeMarker.getLatLng())) {
                this.markerInfo(marker);
                delete this.activeMarker;
            }
        }
        
        // Create popup and open it up when user clicks on marker.
        //marker.bindPopup();
        marker.on('click', function () {
            this.markerInfo(marker);
        }.bind(this));
    };
    
    // Delete single marker
    // 
    // @param marker { object L.marker } Marker object
    
    Map.prototype.deleteMarker = function (marker) {
        this.markers.splice(this.markers.indexOf(marker), 1);
        this.map.removeLayer(marker);
    };
    
    // Clear entire marker collection
    
    Map.prototype.clearMarkers = function () {
        _.each(this.markers, function (marker) {
            this.map.removeLayer(marker);
        }, this);
        this.markers = [];
    };
    
    // Method to open popup with detailed info about marker object.
    //
    // @param marker { L.marker } Single marker object
    
    Map.prototype.markerInfo = function (marker) {
        $.get(this.opts.infoURL, marker.meta, function (response) {
            var popup = null,
                model = CONTENT_TYPES[marker.meta.ct].model,
                tpl = (model === 'location') ? '#loc-dialog-tpl'
                                             : '#map-dialog-tpl';
            // We have to create different template for location objects
            tpl = _.template($(tpl).html());
            // Little hack for template - is it really necessary?
            response[0].content_object.content_type = marker.meta.ct;
            popup = L.popup({minWidth: 500, maxWidth: 500});
            popup.setContent(tpl(response[0].content_object))
                .setLatLng(marker.getLatLng())
                .openOn(this.map);
        }.bind(this));
    };
    
    // Set filters to search only for markers related to selected content types
    //
    // @param filters { array/int/null } Single type id or array of id's. Pass null to clear.

    Map.prototype.setFilters = function (filters) {
        if (filters === undefined) return false;
        if (_.isNull(filters)) {
            // Reset filters
            this.filters = [];
        } else if (_.isArray(filters)) {
            // Array of filters
            this.filters = filters;
        } else {
            // Single filter
            this.filters = [filters];
        }
        this.fetchData();
    };
    
    // Set filter to search only for objects related to selected location.
    //
    // @param location { int } Location's ID. null to reset.
    
    Map.prototype.setLocation = function (location) {
        if (_.isNull(location)) {
            this.location = null;
            return true;
        }
        this.location = location.location;
        this.map.setView([location.lat, location.lng], 10);
        this.fetchData();
    };
    
    return Map;
    
});