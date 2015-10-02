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
        'js/modules/mapvotes/manage-map/form',
        'js/modules/mapvotes/manage-map/modal'],

function ($, _, Backbone, createMap,
          MarkerCollection, Marker, MarkerForm, ModalForm) {

"use strict";

function Map (options) {
  this.map = createMap(options);
  this.map.on('click', this.addMarker.bind(this));
  this.collection = new MarkerCollection(options.markers);
  this.collection.url = options.apiUrl;
  this.form = new MarkerForm({
    el: '#va__description'
  });
  this.modal = new ModalForm({
    el: '#va__modal',
    collection: this.collection
  });
  this.listenTo(this.modal, 'submit', this.newItem);
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
    map: this.map
  });
  m.marker.addTo(this.map);
  this.listenTo(m, 'activated', this.renderDetails);
  return m;
};

Map.prototype.newItem = function (item) {
  var m = this.renderItem(item);
  this._active = item.get('id');
  this.form.model = item;
  this.form.render();
};

Map.prototype.renderDetails = function (model) {
  this._active = model.get('id');
  this.form.model = this.collection.get(this._active);
  this.form.render();
};

Map.prototype.addMarker = function (e) {
  this.modal.open({
    lat: e.latlng.lat.toFixed(6),
    lng: e.latlng.lng.toFixed(6)
  });
};

_.extend(Map.prototype, Backbone.Events);

return Map;

});

