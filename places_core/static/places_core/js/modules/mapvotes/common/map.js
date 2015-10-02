/**
 * vote-map.js
 * ===========
 *
 * Map for voting.
 */

define(['jquery',
        'underscore',
        'leaflet'],

function ($, _, L) {

"use strict";

// Default settings for Leaflet map

var defaults = {

  // Map DOM element ID attribute (REQUIRED!)
  elementID: 'map',

  // Width for map container
  width: 400,

  // Height for map container
  height: 300,

  // URL for map tiles
  tailURL: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

  // Minimum zoom level
  minZoom: 9,

  // Maximum zoom level - should be adjusted depending on tiles in use
  maxZoom: 18,

  // Initial zoom level
  startZoom: 12,

  // Detect retina for graphics
  detectRetina: true,

  // Initial position - latitude
  centerX: 0,

  // Initial position - longitude
  centerY: 0,

  // Map attribution
  attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
};

L.Icon.Default.imagePath = CivilApp.staticURL + '/includes/leaflet/images/';

// Set currently active location position if it is available. If not, try to
// find user's position via Geolocation API.
//
// TODO: find user via Geolocation API.

function getPosition () {
  var lat, lng;
  if (!_.isUndefined(CivilApp.currentLocation)) {
    lat = parseFloat(CivilApp.currentLocation.lat);
    lng = parseFloat(CivilApp.currentLocation.lng);
    return [lat, lng];
  }
  return false;
}

// Reusable wrapper for Leaflet map allowing us to set some custom settings.

function createMap (options) {
  options = _.extend(defaults, options);
  var center = getPosition() || [options.centerX, options.centerY];
  $('#' + options.elementID).css({
    width: options.width + 'px',
    height: options.height + 'px'
  });
  var map = L.map(options.elementID)
    .setView(center, options.startZoom);
  L.tileLayer(options.tailURL, {
    attribution: options.attribution,
    maxZoom: options.maxZoom,
    detectRetina: options.detectRetina
  }).addTo(map);
  return map;
}

return createMap;

});

