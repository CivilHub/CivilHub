//
// area-finder.js
// ==============

// Test script that uses mapinput and new spacial library from gadm
// to look for admin areas for selected lat/lng pairs.

define(['jquery',
        'underscore',
        'text!tpl/adminarea-search-result.html',
        'js/modules/ui/mapinput'],

function ($, _, html) {

"use strict";

function fetchData (lat, lng, fn, context) {
  $.get('/api-geonames/admin-areas/', { lat: lat, lng: lng },
    function (response) {
      fn.call(context, response);
    });
}

function AreaFinder (elID) {
  this.template = _.template(html);
  _.bindAll(this, 'search');
  this.$el = $(document.getElementById(elID));
  this.$el.mapinput({
    width: 600,
    height: 450,
    iconPath: CivilApp.staticURL + '/css/images',
    onchange: this.search
  });
}

AreaFinder.prototype.search = function (m) {
  fetchData(m.lat, m.lng, function (response) {
    _.extend(response, {
      lat: m.lat.toFixed(4),
      lng: m.lng.toFixed(4)
    });
    $('#search-adminarea-results')
      .html(this.template(response));
  }, this);
};

return AreaFinder;

});
