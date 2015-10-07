/**
 * manage-map.js
 * =============
 *
 * Manage markers for voting.
 */

require(['jquery',
         'js/modules/mapvotes/manage-map/application'],

function ($, Map) {

"use strict";

var options = {
  elementID: 'va__map',
  apiUrl: '/api-mapvotes/markers/',
  markers: VA__MAP_DATA.markers,
  tailURL: 'https://b.tiles.mapbox.com/v4/grzegorz21.k01pjfol/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3J6ZWdvcnoyMSIsImEiOiJPX0F1MWJvIn0.sciNGCKR54oCVhfSYPFCCw'
}

$(document).ready(function () {
  var map = new Map(options);
});

});
