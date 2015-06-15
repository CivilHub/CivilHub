//
// visitors.js
// ===========

// Manages map showing users currently on page.

require(['jquery',
         'underscore',
         'backbone',
         'leaflet'],

function ($, _, Backbone, L, http) {

"use strict";

var VisitorsMap = Backbone.View.extend({
  initialize: function () {
    var markers = [];
    _.each(JSON.parse(this.$el.attr('data-markers')), function (data, pk) {
      if (_.isEmpty(data)) {
        return;
      }
      data.id = Number(pk);
      markers.push(data);
    });
    this.collection = new Backbone.Collection(markers);
    console.log(this.collection);
  }
});

$(document).ready(function () {
  var testMap = new VisitorsMap({
    el: '#map'
  });
});

});
