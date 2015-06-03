//
// vote-summary.js
// ===============

// List of users that voted for single comment.

define(['jquery',
        'underscore',
        'backbone',
        'text!js/modules/inlines/templates/summary-entry.html',
        'bootstrap'],

function ($, _, Backbone, entryTPL) {

"use strict";

// Wrapper for setTimeout that allows us to pass context into callback function.
//
// @param Number   Total number of miliseconds for timeout
// @param Function Callback function to trigger
// @param Object   Context object to pass as 'this' (optional)
//
// @returns Timeout

function delay(timeout, callback, context) {
  return setTimeout(function () {
    if (_.isFunction(callback)) {
      callback.call(context);
    }
  }, timeout);
}

// Simple view for single user item.

var Vote = Backbone.View.extend({

  tagName: 'li',

  template: _.template(entryTPL),

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  }
});

// Main summary window object
//
// OPTIONS:
//  - element   DOM element to use for window
//  - vote      Vote 'up' or 'down'
//  - itemID    Comment's unique ID
//  - odDestroy Callback to trigger when window is destroyed

var VoteSummary = Backbone.View.extend({

  initialize: function (options) {
    this.clock = null;
    this.$el = $(options.element);
    this.vote = options.vote || 'all';
    this.itemID = options.itemID || 0;
    this.onDestroy = options.onDestroy || null;
    this.collection = new Backbone.Collection();
    this.collection.url = ([
      '/api-comments/list/', this.itemID,
      '/summary/?v=', this.vote]).join('');
    this.listenTo(this.collection, 'sync', this.render);
    this.collection.fetch();
  },

  render: function () {
    this.collection.each(function (item) {
      this.renderItem(item);
    }, this);
    this.$el.fadeIn('fast');
    this.setClock();
    this.$el.one('mouseenter', this.onMouseEnter.bind(this));
  },

  onMouseEnter: function (e) {
    e.stopPropagation();
    this.stopClock();
    this.$el.off('mouseenter');
    this.$el.one('mouseleave', this.onMouseOut.bind(this));
  },

  onMouseOut: function (e) {
    e.stopPropagation();
    this.setClock();
    this.$el.off('mouseleave');
    this.$el.one('mouseenter', this.onMouseEnter.bind(this));
  },

  setClock: function () {
    this.clock = delay(1000, this.destroy, this);
  },

  stopClock: function () {
    clearTimeout(this.clock);
  },

  renderItem: function (item) {
    var vote = new Vote({ model: item });
    $(vote.render().el).appendTo(this.$el);
  },

  destroy: function () {
    this.$el.fadeOut('fast', function () {
      this.$el.empty()
        .off('mouseenter')
        .off('mouseleave');
      if (_.isFunction(this.onDestroy)) {
        this.onDestroy();
      }
    }.bind(this));
  }
});

return VoteSummary;

});
