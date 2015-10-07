/**
 * map.js
 * ======
 *
 * Main application controller.
 */

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/mapvotes/common/map',
        'js/modules/mapvotes/common/collection',
        'js/modules/mapvotes/common/marker',
        'js/modules/mapvotes/vote-map/detail'],

function ($, _, Backbone, createMap,
          MarkerCollection, Marker, DetailView) {

"use strict";

function Map (options) {
  this.map = createMap(options);
  this.collection = new MarkerCollection(options.markers);
  this.collection.url = options.apiUrl;
  this.details = new DetailView({
    el: '#va__description'
  });
  this.render();
}

Map.prototype.render = function () {
  this.collection.each(function (item) {
    this.renderItem(item);
  }, this);
};

Map.prototype.renderItem = function (item) {
  var m = new Marker({
    model: item,
    map: this.map,
    clickable: true
  });
  m.marker.addTo(this.map);
  this.listenTo(m, 'activated', this.renderDetails);
};

Map.prototype.renderDetails = function (model) {
  this._active = model.get('id');
  this.details.model = this.collection.get(this._active);
  this.details.render();
};

_.extend(Map.prototype, Backbone.Events);

return Map;

});

