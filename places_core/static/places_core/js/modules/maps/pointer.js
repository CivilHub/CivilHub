//
// pointer.js
// ==========

// Script to load when you want to use map pointer form.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'js/modules/ui/ui',
         'bootstrap',
         'js/modules/ui/mapinput'],

function ($, _, utils, ui) {

"use strict";

var BASE_URL = '/api-maps/objects/?ct={ct}&pk={id}';
var ICON_URL = mapApp.staticUrl + '/css/images';

function Minimap (el) {
  this._state = false;
  this.$toggle = $(el);
  this.$modal = $('#minimap-modal');
  this.$submit = this.$modal.find('[type="submit"]');
  this.$input = this.$modal.find('#minimap');
  this.ct = this.$toggle.attr('data-ct');
  this.pk = this.$toggle.attr('data-id');
  this.url = BASE_URL
    .replace(/{ct}/g, this.ct)
    .replace(/{id}/g, this.pk);
}

Minimap.prototype.initialize = function () {
  this.$modal.on('hidden.bs.modal', function () {
    this._state = false;
  }.bind(this));
  this.$modal.on('shown.bs.modal', function () {
    this.setMapInput();
  }.bind(this));
  this.$submit.on('click', function (e) {
    e.preventDefault();
    this.sendMarkers();
  }.bind(this));
};

// We need this method to run AFTER modal is opened, in other case
// there are some issues with proper size and look of minimap.

Minimap.prototype.setMapInput = function () {
  var $mapinput = this.$input;
  if (!_.isUndefined($mapinput.data('mapinput'))) {
    return true;
  }
  $.get(this.url, function (markers) {
    $mapinput.mapinput({
      single: false,
      width: 550,
      height: 300,
      markers: markers,
      iconPath: ICON_URL
    });
  });
};

Minimap.prototype.sendMarkers = function () {
  var mapinput = this.$input.data('mapinput');
  var markers = $.map(mapinput.markers, function (marker) {
    return {lat: marker.getLatLng().lat, lng: marker.getLatLng().lng};
  });
  var data = {
    csrfmiddlewaretoken: utils.getCookie('csrftoken'),
    content_type: this.ct,
    object_pk: this.pk,
    markers: JSON.stringify(markers)
  };
  $.post('/api-maps/mapinput/', data, function (response) {
    if (response.success) {
      ui.message.success(response.message);
    } else {
      ui.message.danger(response.message);
    }
  });
  // TODO: we assume that everything goes well.
  // This is not good approach, but sufficient for now.
  this._close();
};

Minimap.prototype._open = function () {
  this.$modal.modal('show');
  this._state = true;
};

Minimap.prototype._close = function () {
  this.$modal.modal('hide');
  this._state = false;
};

Minimap.prototype.toggle = function () {
  if (this._state === true) {
    this._close();
  } else {
    this._open();
  }
};

$.fn.minimapToggler = function () {
  return $(this).each(function () {
    var map = new Minimap(this);
    $(this).data('minimap', map);
    $(this).on('click', function (e) {
      e.preventDefault();
      map.toggle();
    });
    map.initialize();
  });
};

$(document).ready(function () {
  $('.map-marker-toggle').minimapToggler();
});

});
