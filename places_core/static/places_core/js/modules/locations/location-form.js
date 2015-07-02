//
// location-form.js
// ================

// Scripts to handle location form. This script includes two simple Backbone
// views to handle simplified parent location selection.

// TODO: fill initial parent value and create proper inputs.

require(['jquery',
         'underscore',
         'backbone',
         'text!tpl/fake-input.html',
         'js/modules/ui/mapinput'],

function ($, _, Backbone, inputTPL) {

"use strict";

// Common function to perform GET requests from within application.
//
// @param { String } Target url
// @param { Object } GET parameters in object notation
// @param { Function } Callback to use on success
// @param { Object } Context object to pass as "this"

function fetchData (url, data, fn, context) {
  $.get(url, data, function (response) {
    fn.call(context, response);
  });
}

// Represents single location selection button

var FakeInput = Backbone.View.extend({

  baseURL: '/api-locations/sublocations/',

  className: 'fake',

  expanded: false,

  events: {
    'click .input-indicator': 'toggleList',
    'keyup .search-filter': 'filter'
  },

  initialize: function (options) {
    _.bindAll(this, 'toggleList');
    this.onFetch = options.onFetch || null;
    this.model = new Backbone.Model();
    this.model.set({ id: options.id, label: options.label });
    this.template = _.template(inputTPL);
  },

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  },

  toggleList: function () {
    this.fetch();
    this.$el.find('ul')
      .fadeToggle('fast');
  },

  fetch: function () {
    var data = { pk: this.model.get('id') };
    if (this.expanded) {
      return;
    }
    fetchData(this.baseURL, data, function (r) {
      _.each(r, function (location) {
        this.appendOption(location.id, location.name);
      }, this);
      this.expanded = true;
      if (_.isFunction(this.onFetch)) {
        this.onFetch(this);
      }
    }, this);
  },

  appendOption: function (id, label) {
    var html = '<li class="name-entry" data-value="' +
               '<%= id %>"><%= label %></li>';
    var tpl = _.template(html);
    var $opt = $(tpl({ id: id, label: label }));
    $opt.on('click', function (e) {
      e.preventDefault();
      this.$el.nextAll('.fake').empty().remove();
      this.toggleList();
      if (!_.isUndefined(this.parent)) {
        this.parent.addInput(id, label);
      }
    }.bind(this));
    this.$el.find('ul').append($opt);
  },

  filter: function () {
    var term = this.$('.search-filter').val();
    var re = new RegExp(term, 'i');
    _.each(this.$el.find('.name-entry'), function (el) {
      if (re.test($(el).text())) {
        $(el).show();
      } else {
        $(el).hide();
      }
    }, this);
  }
});

// Represents entire location form

var LocationForm = Backbone.View.extend({

  el: '#new-location-form',

  baseURL: '/api-locations/find-nearest/',

  events: {
    'click .country-selector': 'toggleCountries',
    'click .country-entry': 'selectCountry'
  },

  initialize: function (options) {
    _.bindAll(this, 'fetch');
    _.bindAll(this, 'selectCountry');
    this.$el = $('#' + options.id);
    this.$map = $('<div id="map"></div>');
    this.$map.insertBefore(this.$('#id_latitude'));
    var mapOpts = {
      single: true,
      width : 664,
      height: 480,
      markers: CivilApp.markers,
      iconPath: ([CivilApp.staticURL, 'css', 'images']).join('/'),
      onchange: this.fetch
    };
    var initLat = this.$('#id_latitude').val();
    var initLng = this.$('#id_longitude').val();
    if (initLat && initLng) {
      mapOpts = _.extend(mapOpts, {
        center: [initLat, initLng],
        markers: [{ lat: initLat, lng: initLng }]
      });
    }
    this.$map.mapinput(mapOpts);

    // Fill initial parent values

    var initial = this.$el.attr('data-initial');
    if (initial.length > 0) {
      this.reset();
      _.each(JSON.parse(initial).reverse(), function (item) {
        this.addInput(item.id, item.label);
      }, this);
    }
  },

  fetch: function (e) {
    var data = { lat: e.lat, lng: e.lng };
    this.reset();
    fetchData(this.baseURL, data, function (r) {
      this.addInput(r.country.id, r.country.name);
      this.addInput(r.region.id, r.region.name);
      this.$('#id_latitude').val(e.lat);
      this.$('#id_longitude').val(e.lng);
    }, this);
  },

  addInput: function (id, label, options, fn) {
    var opts = options || { onFetch: null };
    var i = new FakeInput({
      id: id,
      label: label,
      onFetch: opts.onFetch
    });
    i.parent = this;
    $(i.render().el)
      .appendTo(this.$('.fake-input-placeholder'));
    this.$('#id_parent').val(id);
    if (_.isFunction(fn)) {
      fn.call(this, i);
    }
  },

  reset: function () {
    this.$el.find('.fake').empty().remove();
  },

  toggleCountries: function () {
    this.$('.country-selector')
      .next('.sublist')
      .fadeToggle('fast');
  },

  selectCountry: function (e) {
    var id = $(e.target).attr('data-value');
    var label = $(e.target).text();
    this.reset();
    this.addInput(id, label, {
      onFetch: function (input) {
        var id = input.$el.find('.name-entry:first').attr('data-value');
        var label = input.$el.find('.name-entry:first').text();
        input.parent.addInput(id, label);
      }
    }, function (input) {
      input.fetch();
    });
  },

  fillInitial: function (initial) {
    var url = '/api-locations/locations/' + initial + '/';
    fetchData(url, null, function (r) {
      this.addInput(r.id, r.name);
    });
  }
});

$(document).ready(function () {
  var form = new LocationForm({ id: 'new-location-form' });
});

});
