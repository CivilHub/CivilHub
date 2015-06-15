//
// vote-summary.js
// ===============

// List of users that voted for single comment.

define(['jquery',
        'underscore',
        'backbone',
        'text!js/modules/inlines/templates/summary-entry.html'],

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

// Main summary window controller. You may pass options (actually, you have to
// provide at least comment ID, the rest is optional, but usefull.

var VoteSummary = Backbone.View.extend({

  tagName: 'ul',

  className: 'comment-vote-summary',

  onDestroy: null,

  clock: null,

  initialize: function (options) {
    this.collection = new Backbone.Collection();
    this.collection.url = ([
      '/api-comments/list/', options.data.id,
      '/summary/?v=', options.data.vote]).join('');
    this.listenTo(this.collection, 'sync', this.render);
    this.collection.fetch();
    if (!_.isUndefined(options.position)) {
      this.position = options.position;
    }
    this.setClock();
  },

  render: function (collection) {
    if (collection.length === 0) {
      return;
    }
    this.$el.appendTo('body');
    if (!_.isUndefined(this.position)) {
      this.$el.offset(this.position);
    }
    this.$el.fadeIn('fast');
    this.collection.each(function (item) {
      this.renderVote(item);
    }, this);
  },

  renderVote: function (item) {
    var view = new Vote({ model: item });
    $(view.render().el).appendTo(this.$el);
  },

  setClock: function () {
    this.clock = delay(1000, this.destroy, this);
    this.$el.one('mouseenter', function () {
      clearTimeout(this.clock);
      this.$el.one('mouseleave', this.setClock.bind(this));
    }.bind(this));
  },

  destroy: function () {
    this.$el.fadeOut('slow', function () {
      this.$el.empty().remove();
      if (_.isFunction(this.onDestroy)) {
        this.onDestroy();
      }
    }.bind(this));
  }
});

return VoteSummary;

});
