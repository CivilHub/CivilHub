/**
 * marker.js
 * =========
 *
 * This is binding between ``Leaflet.Marker`` and ``Backbone.View``.
 */

define(['jquery',
        'leaflet',
        'underscore',
        'backbone'],

function ($, L, _, Backbone) {

"use strict";

// Template for popup window content

var TEMPLATE = _.template(([
  '<h4><%= label %></h4>',
  '<div><%= description %></div>'
]).join("\n"));

// Initializer - this constructor shadows a lot of Backbone's View
// functionality and takes similar options. The most important are
// ``model`` and ``map``. Without them it will not work.

function Marker (options) {
  this.model = options.model;
  this.map = options.map;
  this.clickable = options.clickable || false;
  var position = [this.model.get('lat'), this.model.get('lng')];
  this.marker = L.marker(position, {
    title: this.model.get('label')
  });
  this.marker.on('click', this.showInfo.bind(this));
  this.listenTo(this.model, 'destroy', this.remove);
}

// Opens popup window with detailed info
// and triggers ``activated`` event.

Marker.prototype.showInfo = function () {
  this.trigger('activated', this.model);
  if (!this.clickable) return;
  var popup = L.popup()
    .setContent(TEMPLATE(this.model.toJSON()))
    .setLatLng([this.model.get('lat'), this.model.get('lng')])
    .openOn(this.map);
};

Marker.prototype.remove = function () {
  this.map.removeLayer(this.marker);
};

_.extend(Marker.prototype, Backbone.Events);

return Marker;

});

