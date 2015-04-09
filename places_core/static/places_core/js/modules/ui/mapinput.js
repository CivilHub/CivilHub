//
// mapinput.js
// ===========

// Simple widget replacing form fields with map
// powerede by Leaflet and Openstreetmaps.

require(['jquery', 'leaflet'],

function ($, L) {
        
"use strict";

$.fn.mapinput = function (options) {

  var defaults = {
      center     : [0, 0],
      zoom       : 2,
      maxZoom    : 18,
      width      : 300,
      height     : 300,
      single     : true,
      markers    : [],
      maxMarkers : 10,
      onchange   : null,
      onexceed   : null,
      ondelete   : null,
      onclear    : null,
      iconPath   : 'default',
      exceedMsg  : "Maximum number of markers exceeded. Remove some to add more",
      tileUrl    : 'https://b.tiles.mapbox.com/v4/grzegorz21.k01pjfol/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3J6ZWdvcnoyMSIsImEiOiJPX0F1MWJvIn0.sciNGCKR54oCVhfSYPFCCw',
      attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
  };

  var opts = $.extend(defaults, options);

  var mapinput = {

    initialize: function ($el) {
      var _self = this;
      var $map = $(document.createElement('div'));
      var elId = "mapinput-" + Math.floor(Math.random() * 1000);

      // Create and adjust DOM element

      this.markers = [];
      this.$el = $el;
      this.$el.attr('id', elId)
        .css('width', opts.width)
        .css('height', opts.height)
        .data('mapinput', this);
      this.$el.children().hide();
      this.$el.append($map);

      // Fix marker icon image path in case that auto-detect not working
      
      if (opts.iconPath !== 'default')
        L.Icon.Default.imagePath = opts.iconPath;

      // Create Leaflet map

      this.map = L.map(elId).setView(opts.center, opts.zoom);
        L.tileLayer(opts.tileUrl, {
        attribution: opts.attribution,
        maxZoom: opts.maxZoom
      }).addTo(this.map);

      // Handle map events

      this.map.on('click', function (e) {
        _self.handleEvent(e);
      });

      // Create initial markers (if there are any)

      $.each(opts.markers, function (idx, marker) {
        this.addMarker(marker.lat, marker.lng);
      }.bind(this));
    },

    handleEvent: function (e) {
      var lat = e.latlng.lat;
      var lng = e.latlng.lng;

      if (opts.single) {
        // Single marker option enabled
        this.clear();
      } else if (this.markers.length >= opts.maxMarkers) {
        // Exceeded maximum number of markers
        alert(opts.exceedMsg);
        if (opts.onexceed !== null && typeof(opts.onexceed === 'function')) {
          opts.onexceed(e);
        }
        return false;
      }

      this.addMarker (lat, lng);

      if (opts.onchange !== null && typeof(opts.onchange === 'function')) {
        // Common change event to fire on every occasion
        opts.onchange({'lat': lat, 'lng': lng}, this.markers);
      }
    },

    addMarker: function (lat, lng) {
      var _self = this;
      var marker = L.marker([lat, lng]).addTo(this.map);
      marker.on('click', function (e) {
        _self.deleteMarker(marker);
      });
      this.markers.push(marker);
      return marker;
    },

    clear: function () {
      $.each(this.markers, function (idx, marker) {
        this.map.removeLayer(marker);
      }.bind(this));
      this.markers = [];

      if (opts.onclear !== null && typeof(opts.onclear === 'function')) {
        // Common change event to fire on every occasion
        opts.onclear();
      }
    },

    deleteMarker: function (marker) {
      var idx = this.markers.indexOf(marker);
      this.map.removeLayer(marker);
      this.markers.splice(idx, 1);

      if (opts.ondelete !== null && typeof(opts.ondelete === 'function')) {
        opts.ondelete({
          'lat': marker.getLatLng().lat,
          'lng': marker.getLatLng().lng
        }, this.markers);
      }

      // FIXME: try to handle this only in click event handler

      if (opts.onchange !== null && typeof(opts.onchange === 'function')) {
        // Common change event to fire on every occasion
        opts.onchange({
          'lat': marker.getLatLng().lat,
          'lng': marker.getLatLng().lng
        }, this.markers);
      }
    }
  };

  // Initialize plugin on current element

  return $(this).each(function () {
    var $el = $(this);
    var map = mapinput;
    map.initialize($el);
    $(this).data('mapinput', map);
  });
};

});