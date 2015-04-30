//
// col-view.js
// ============

// A single collumn view bound to a certain location. Here we show a list
// of all locations that "inherit" from the previously selected (or from
// a selected country, if it is a single collumn).

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/locations/location-list/location-collection',
        'js/modules/locations/location-list/location-list-view'],

function ($, _, Backbone, LocationCollection, LocationListView) {

"use strict";

var ColView = Backbone.View.extend({

  tagName: 'ul',

  className: 'list-column col-sm-3',

  template: _.template($('#list-col-tpl').html()),

  events: {
    'click .expand-entry': 'expand',
    'click .close-col': 'destroy'
  },

  items: {}, // A placeholder for views connected with collection models.

  initialize: function () {
    // TODO: erorr interception when wrong arguments were passed.
    this.locationID = arguments[1];
    this.tier = arguments[2];
    this.collection = new LocationCollection();
    this.collection.url =
        '/api-locations/sublocations/?pk=' + this.locationID;
    this.collection.fetch();
    this.listenTo(this.collection, 'sync', this.render);
  },

  render: function () {
    var self = this;
    this.$el.appendTo('#list-placeholder > .placeholder-content');
    if (this.collection.length >= 1) {
      this.$el.html(this.template({ tier: this.tier }));
      this.collection.each(function (item) {
        this.renderEntry(item);
      }, this);
    }
    this.$el.addClass('tab-offset-' + this.tier);
    this.$el.find('.search-entry').on('keyup', function (e) {
      self.filter($(this).val());
    });
  },

  renderEntry: function (item) {
    var entry = new LocationListView({
      model: item
    });
    var $el = $(entry.render().el);
    entry.parentView = this;
    this.items[item.get('id')] = entry;
    $el.appendTo(this.$el);
  },

  filter: function (s) {
    var re = new RegExp(s, 'i');
    var model = null;
    _.each(this.items, function (item, idx) {
      model = this.collection.get(idx);
      // FIXME: Views Collecions seem to join into one, which results
      // in checking non-existing elements.
      if (model === undefined) return false;
      if (!re.test(model.get('name'))) {
        item.hide();
      } else {
        item.show();
      }
    }, this);
  },

  expand: function (e) {
    e.preventDefault();
    // If the sub-location list is opened, we do not open it again.
    if (this.sublist !== undefined) {
      return false;
    }
    var id = $(e.currentTarget).attr('data-target');
    this.items[id].details();
    this.$el.scrollTop(0); // Hack for google-chrome
    this.sublist = new ColView([], id, this.tier + 1);
    this.listenTo(this.sublist.collection, 'sync', function () {
      // We check if this element has any other nested locations
      // IF not, we delete the lisst. Same thing applies to last
      // last nested
      if (!this.sublist.collection.length > 0 || this.tier >= 3) {
        this.sublist.$el.empty().remove();
        delete this.sublist;
        this.$el.addClass('is-last-entry');
        $($('#empty-tpl').html()).insertAfter(this.$el);
      } else {
        this.sublist.parentView = this;
        this.$el.removeClass('is-last-entry');
      }
    });
  },

  cleanDetails: function () {
    _.each(this.items, function (item, index) {
      if (this.collection.get(index) !== undefined) {
        item.hideDetails();
      }
    }, this);
  },

  destroy: function () {
    this.$el.fadeOut('fast', function () {
      this.$el.empty().remove();
    }.bind(this));
    if (this.sublist !== undefined) {
      this.sublist.destroy();
    }
    if (this.parentView != undefined) {
      // Sublist - delete it from the 'master' index
      delete this.parentView.sublist;
      // Hide details of previous elements
      this.parentView.cleanDetails();
    } else {
      // First, basic list. We emit a signal and close
      // the window with location browser.
      this.trigger('destroyed');
    }
  }
});

return ColView;

});
