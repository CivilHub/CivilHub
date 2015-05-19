//
// city-finder.js
// ==============

// Search for nearest important city. Useful for create location form,
// where we can select parents based on places selected on map by user.

define(['jquery',
        'underscore',
        'text!tpl/city-search-result.html',
        'js/modules/ui/mapinput'],

function ($, _, html) {

"use strict";

function fetchData (lat, lng, fn, context) {
  $.get('/api-locations/find-nearest/', { lat: lat, lng: lng },
    function (response) {
      fn.call(context, response);
    });
}

function CityFinder (elID) {
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

CityFinder.prototype.search = function (m) {
  fetchData(m.lat, m.lng, function (response) {
    _.extend(response, {
      lat: m.lat.toFixed(4),
      lng: m.lng.toFixed(4)
    });
    $('#search-adminarea-results')
      .html(this.template(response));
  }, this);
};

return CityFinder;

});
