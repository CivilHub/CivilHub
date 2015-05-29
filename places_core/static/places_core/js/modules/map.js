//
// map.js
// ======

// Load modules for main map view.

require(['jquery',
         'underscore',
         'js/modules/maps/map'],

function ($, _, CivilMap) {

"use strict";

// Fallback - default initial map center provided by GeoIP.
// All initial data is prepared in map template HTML file.

var DP = {
  lat: CIVILAPP.position.lat,
  lng: CIVILAPP.position.lng
};

// Translates data-target attribute to content type ID
//
// @param string CT specs in <app_label>.<model_name> format.

function getContentType (label) {
  var app = label.split('.')[0];
  var model = label.split('.')[1];
  var type = _.find(CONTENT_TYPES, function (t) {
    return t.app_label == app && t.model == model;
  });
  if (_.isUndefined(type)) {
    return null;
  }
  return type.content_type;
}

// Initializes entire map application
//
// @param Float Map center's latitude
// @param Float Map center's longitude

function createMap (lat, lng, current) {
  var mapOptions = {
    elementID: 'main-map',
    center: [lat, lng],
    mapTailURL: 'https://b.tiles.mapbox.com/v4/grzegorz21.k01pjfol/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3J6ZWdvcnoyMSIsImEiOiJPX0F1MWJvIn0.sciNGCKR54oCVhfSYPFCCw'
  };
  if (!_.isUndefined(current)) {
    mapOptions = _.extend(mapOptions, {
      startZoom: 15,
      active: current
    });
  }
  var map = new CivilMap(mapOptions);
  var $boxes = $('.map-filter-toggle');
  $boxes.on('click', function (e) {
    var types = [];
    $boxes.each(function () {
      if ($(this).is(':checked')) {
        types.push(getContentType($(this).attr('data-target')));
      }
    });
    map.filter(types);
  });
  window.test = map;
}

// Use this function if user's browser supports geolocation and he/she
// agreed to share location.
//
// @param Geopostion Geoposition object returned by geolocation API.

function initCallback (position) {
  return createMap(position.coords.latitude, position.coords.longitude);
}

// Use this function to create map centered in location pointed by GeoIP.

function initFallback () {
  return createMap(DP.lat, DP.lng);
}

// Get visitor's geoposition
//
// @param Function Callback to trigger on success
// @context Object Pass context object if you want to bind 'this' value

function getCoords (callback, context) {
  if (!Modernizr.geolocation) {
    return createMap(DP.lat, DP.lng);
  }
  navigator.geolocation.getCurrentPosition(initCallback, initFallback);
}

// Move all event binding and everything DOM-related here.

$(document).ready(function () {
  if (!_.isUndefined(CIVILAPP.current)) {
    createMap(CIVILAPP.current.latitude, CIVILAPP.current.longitude, CIVILAPP.current);
  } else {
    getCoords();
  }
  $('.angle-icon-toggle').on('click', function (e) {
    e.preventDefault();
    $('#map-options-panel').slideToggle('fast');
  });
});

});
