//
// map.js
// ======

// Scripts to handle new version of main map.

define(['jquery',
        'underscore',
        'leaflet',
        'text!js/modules/maps/templates/map-object.html',
        'text!js/modules/maps/templates/map-location.html'],

function ($, _, L, oTpl, lTpl) {

"use strict";

var defaults = {

  // Id attribute of element for map - mandatory
  elementID: 'map',

  // Base url to get marker data
  apiURL: '/api-maps/new-markers/',

  // URL to fetch info about specific object
  infoURL: '/api-maps/objects/',

  // Change this value if you want to use custom tile set
  mapTailURL: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

  // Minimum zoom to show single markers
  minZoom: 9,

  // Maximum possible zoom - because of tileset settings
  maxZoom: 18,

  // List of content types id to fetch
  filters: [],

  // Use Leaflet detect retina feature
  detectRetina: true,

  // Initial default zoom
  startZoom: 12,

  // Initial center position
  center: [0, 0],

  // Active marker used for centering map from outer views ("show on map")
  active: null,

  // Attribution to display in map area
  attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
};

// Array that will hold icon metadata

var icons = [];

// Create icons for different marker types

_.each(CIVILAPP.icons, function (icon, key) {
  icons[key] = L.icon(icon);
});

// Common shortcut for jQuery GET function taking callback as argument. You can
// also pass 'context' argument, which simplify passing 'this' value.
//
// @param String Url to send data
// @param Object GET request data in form of plain object
// @param Function Callback to trigger on success
// @param Object   Context to pass as 'this' to callback.

function fetch (url, data, callback, context) {
  $.get(url, data, function (response) {
    if (_.isFunction(callback)) {
      callback.call(context, response);
    }
  });
}


// -----------------------------------------------------------------------------
//
// Custom wrapper for Leaflet marker
//
// -----------------------------------------------------------------------------

function MapMarker (item) {

  // This value should be set by parent object in initialize method.
  this.apiUrl = '/';

  this.marker = L.marker([item.latitude, item.longitude], {
    icon: icons[item.content_type]
  });

  this.marker.on('click', function (e) {
    this.getInfo();
  }.bind(this));

  this.meta = {
    id: item.id,
    ct: item.content_type,
    pk: parseInt(item.object_pk, 10)
  };
}

// Allows us to pass some additional options from main map object
//
// @param Object Plain object with additional parameters

MapMarker.prototype.initialize = function (options) {
  this.apiUrl = options.apiUrl || defaults.infoURL;
};

// Get detailed info about marked object

MapMarker.prototype.getInfo = function () {
  var data = { ct: this.meta.ct, pk: this.meta.pk };
  var popup = L.popup({ minWidth: 500, maxWidth: 500 });
  fetch(this.apiUrl, data, function (response) {
    var obj = response[0].content_object;
    var tpl = obj.type.kind === 'location' ? lTpl : oTpl;
    tpl = _.template(tpl);
    popup.setContent(tpl(obj))
      .setLatLng(this.marker.getLatLng())
      .openOn(this.marker._map);
  }, this);
};


// -----------------------------------------------------------------------------
//
// Simplified marker representing cluster group
//
// -----------------------------------------------------------------------------

function MapCluster (item) {
  this.marker = L.marker([item.lat, item.lng], {
    icon: L.divIcon({
      className: 'count-icon',
      html: item.count,
      iconSize: [40, 40]
    })
  });
  this.meta = { id: item.id };
}

// Bind events
//
// @param Object Plain object with options - not used for now.

MapCluster.prototype.initialize = function (options) {
  this.marker.on('click', function (e) {
    this.setMapPosition();
  }.bind(this));
};

// Set map position to show underlying markers

MapCluster.prototype.setMapPosition = function () {
  this.marker._map.setView(this.marker.getLatLng(), 12);
};


// -----------------------------------------------------------------------------
//
// Main map object - manages entire map and creates Leaflet objects
//
// @param Object Options in plain object form. They will override 'defaults'
//
// -----------------------------------------------------------------------------

function CivilMap (options) {
  options = _.extend(defaults, options);

  // Collection of markers or clusters
  this.markers = [];

  // Content type filters
  this.filters = options.filters;

  // Zoom value indicating switch markers/clusters
  this.zoomSwitch = options.minZoom;

  // DOM element for entire map
  this.$el = $(document.getElementById(options.elementID));

  // Base URL from which to fetch markers
  this.apiURL = options.apiURL;

  // URL to get detailed info about content object
  this.infoURL = options.infoURL;

  // Create cluster that holds entire single markers collection.
  this.cluster = new L.MarkerClusterGroup();

  // Set initially active marker if you want to open popup on map initialize.
  this.active = options.active;

  // Bind events
  this.initialize(options);
}

// Create Leaflet map and prepare markers to use.
//
// @param Object Options passed by constructor

CivilMap.prototype.initialize = function (options) {
  this.map = L.map(options.elementID)
    .setView(options.center, options.startZoom);

  L.tileLayer(options.mapTailURL, {
    attribution: options.attribution,
    maxZoom: options.maxZoom,
    detectRetina: options.detectRetina
  }).addTo(this.map);

  this.map.addLayer(this.cluster);

  this.fetchData();

  this.map.on('zoomstart', function () {
    this._currentZoom = this.map.getZoom();
  }.bind(this));

  // Control zoom level and change to markers/clusters as needed

  this.map.on('zoomend', function () {
    var i = this._currentZoom;
    var t = this.map.getZoom();

    // This is really strange, but it seems that sometimes
    // in js 'false && true' returns true...

    if (i >= this.zoomSwitch) {
      if (t < this.zoomSwitch) {
        this.clear();
        $('#map-options-toggle').fadeOut('fast');
        $('#map-options-panel').fadeOut('fast');
      }
    } else {
      if (t >= this.zoomSwitch) {
        this.clear();
        $('#map-options-toggle').fadeIn('fast');
        $('#map-options-panel').fadeIn('fast');
      }
    }
    this.fetchData();
    this._currentZoom = t;
  }.bind(this));

  // Mark current boundaries so we can calculate difference later.

  this.map.on('dragstart', function () {
    var bounds = this.map.getBounds();
    this._ne = bounds.getNorthEast();
    this._sw = bounds.getSouthWest();
  }.bind(this));

  // Calculate lat/lng difference to fetch only new markers.

  this.map.on('dragend', function () {
    var bounds = this.map.getBounds();
    var northEast = bounds.getNorthEast();
    var southWest = bounds.getSouthWest();
    var latDiff = northEast.lat - this._ne.lat;
    var lngDiff = northEast.lng - this._ne.lng;
    var ne = {
      lat: this._ne.lat + latDiff,
      lng: this._ne.lng + lngDiff
    };
    var sw = {
      lat: this._sw.lat + latDiff,
      lng: this._sw.lng + lngDiff
    };
    this.fetchData(ne, sw);
  }.bind(this));
};

// Fetch map data when position or zoom changes.

CivilMap.prototype.fetchData = function (ne, sw) {
  var bounds = this.map.getBounds();
  var northEast = ne || bounds.getNorthEast();
  var southWest = sw || bounds.getSouthWest();
  var data = {
    zoom: this.map.getZoom(),
    ne: northEast.lat + 'x' + northEast.lng,
    sw: southWest.lat + 'x' + southWest.lng,
    filters: encodeURIComponent(this.filters)
  };
  fetch(this.apiURL, data, function (response) {
    if (this.map.getZoom() >= this.zoomSwitch) {
      this.renderMarkers(response);
    } else {
      this.renderClusters(response);
    }
  }, this);
};

// Renders entire marker/cluster collection
//
// @param Array Array holding markers fetched from server

CivilMap.prototype.renderMarkers = function (markers) {
  var chk;

  // Create new markers that don't exist yet.

  _.each(markers, function (m) {
    chk = _.find(this.markers, function (marker) {
      return marker.meta.id == m.id;
    });
    if (_.isUndefined(chk)) {
      var marker = new MapMarker(m);
      marker.initialize({ apiUrl: this.infoURL });
      this.markers.push(marker);
      this.cluster.addLayer(marker.marker);
      if (!_.isNull(this.active)) {
        if (m.content_type == this.active.content_type
            && m.object_pk == this.active.object_pk) {
          marker.getInfo();
          this.active = null;
        }
      }
    }
  }, this);

  // Delete objects that are no longer visible

  _.each(this.markers, function (m) {
    chk = _.find(markers, function (marker) {
      return marker.id == m.meta.id;
    });
    if (_.isUndefined(chk)) {
      this.cluster.removeLayer(m.marker);
      this.markers.splice(this.markers.indexOf(m), 1);
    }
  }, this);
};

// Renders simplified markers collection, depending on zoom level
//
// @param Array JSON data fetched from server

CivilMap.prototype.renderClusters = function (clusters) {
  var chk;

  // Similar to the above, but operating on different set of objects

  _.each(clusters, function (c) {
    chk = _.find(this.markers, function (marker) {
      return marker.meta.id == c.id;
    });
    if (_.isUndefined(chk)) {
      var cluster = new MapCluster(c);
      cluster.initialize();
      this.markers.push(cluster);
      this.map.addLayer(cluster.marker);
    }
  }, this);

  // Remove obsolete clusters

  _.each(this.markers, function (m) {
    chk = _.find(clusters, function (cluster) {
      return cluster.id == m.meta.id;
    });
    if (_.isUndefined(chk)) {
      this.map.removeLayer(m.marker);
      this.markers.splice(this.markers.indexOf(m), 1);
    }
  }, this);
};

// Delete single marker and remove it from map
//
// @param L.Marker Marker to delete

CivilMap.prototype.removeMarker = function (m) {
  this.map.removeLayer(m.marker);
  this.markers.splice(this.markers.indexOf(m), 1);
};

// Clear entire collection

CivilMap.prototype.clear = function () {
  this.cluster.clearLayers();
  _.each(this.markers, function (m) {
    this.map.removeLayer(m.marker);
  }, this);
  this.markers = [];
};

// Set filters for content types to narrow results
//
// @param Array List of numeric content type ID's

CivilMap.prototype.filter = function (filters) {
  this.filters = filters;
  this.clear();
  this.fetchData();
};

return CivilMap;

});
