//
// visitors.js
// ===========

// Manages map showing users currently on page.

require(['jquery',
         'underscore',
         'backbone',
         'leaflet',
         'text!js/modules/userspace/templates/visitor-popup.html'],

function ($, _, Backbone, L, tpl) {

"use strict";

// Avoid https://forge.typo3.org/issues/62424

L.Icon.Default.imagePath = CivilApp.staticURL + '/includes/leaflet/images/';

// Some basic options and common "constants"
// -----------------------------------------------------------------------------

var defaults = {
  tileLayer: 'https://b.tiles.mapbox.com/v4/grzegorz21.k01pjfol/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3J6ZWdvcnoyMSIsImEiOiJPX0F1MWJvIn0.sciNGCKR54oCVhfSYPFCCw',
  contribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
  startPosition: [0, 0],
  startZoom: 2,
  maxZoom: 18,
  detectRetina: true
};

var opts = null;

// Util functions for misc purposes
// -----------------------------------------------------------------------------

function fetch (id, fn, ctx) {
  $.get('/tracker/details/' + id + '/', function (response) {
    if (_.isFunction(fn)) {
      fn.call(ctx, response);
    }
  });
}

// Main map object
// -----------------------------------------------------------------------------

var VisitorsMap = Backbone.View.extend({
  initialize: function (options) {
    var config = options.config || {};
    opts = _.extend(defaults, config);
    this.map = L.map(this.$el.attr('id'))
      .setView(opts.startPosition, opts.startZoom);
    this.cluster = new L.MarkerClusterGroup();
    this.initCollection();
    this.render();
  },

  initCollection: function () {
    var markers = [];
    _.each(JSON.parse(this.$el.attr('data-markers')), function (data, pk) {
      if (_.isEmpty(data)) {
        return;
      }
      data.id = Number(pk);
      markers.push(data);
    });
    this.collection = new Backbone.Collection(markers);
  },

  render: function () {
    L.tileLayer(opts.tileLayer, {
      attribution: opts.attribution,
      maxZoom: opts.maxZoom,
      detectRetina: opts.detectRetina
    }).addTo(this.map);
    this.map.addLayer(this.cluster);
    this.collection.each(function (item) {
      this.renderMarker(item);
    }, this);
  },

  renderMarker: function (model) {
    var marker = L.marker([model.get('latitude'), model.get('longitude')]);
    this.cluster.addLayer(marker);
    marker.on('click', function (e) {
      fetch(model.get('id'), function (response) {
        this.infoWindow(marker, response);
      }, this);
    }.bind(this));
  },

  infoWindow: function (marker, data) {
    var popup = L.popup({ minWidth: 500, maxWidth: 500 });
    popup.setContent(_.template(tpl)(data))
      .setLatLng(marker.getLatLng())
      .openOn(this.map);
  }
});

// Run!
// -----------------------------------------------------------------------------

$(document).ready(function () {
  var visitorsMap = new VisitorsMap({ el: '#map' });
});

});
