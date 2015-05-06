//
// actionList.js
// =============

// Entire action list view.

define(['jquery',
        'underscore',
        'backbone',
        'CUri',
        'js/modules/actstream/action-collection',
        'js/modules/actstream/action-view',
        'jpaginate'],

function ($, _, Backbone, CUri, ActionCollection, ActionView) {

"use strict";

var defaults = {
  baseUrl: '/api-activities/actstream/',
  currentPage: 1,
  mode: 'user'
};

var ActionList = Backbone.View.extend({

  el: '.activity-stream',

  currentPage: 1,

  initCollection: function (callback, context) {
    $.get(this.url.url(), function (resp) {
      if (typeof(callback) === 'function') {
        callback.call(context, resp.results, resp.next);
      }
    });
  },

  initialize: function (options) {
    options = _.extend(defaults, options);
    this.currentPage = options.currentPage;
    this.url = new CUri(options.baseUrl);
    this.url.add('type', options.mode);
    this.url.add('ct', options.ct);
    this.url.add('pk', options.pk);
    this.url.add('page', this.currentPage);

    this.collection = new ActionCollection();
    this.collection.url = this.url.url();
    this.listenTo(this.collection, 'add', this.renderItem);
    _.bindAll(this, 'render');
    _.bindAll(this, 'renderPage');
    this.collection.fetch({ success: this.render });

    this.$spinner = $(document.createElement('span'));
    this.$spinner
      .addClass('fa fa-spin fa-circle-o-notch')
      .hide();
  },

  filter: function (content) {
    if (content === 'all') {
      this.url.del('content');
    } else {
      this.url.add('content', content);
    }
    this.currentPage = 1;
    this.url.add('page', this.currentPage);
    this.collection.url = this.url.url();
    this.collection.fetch({ success: this.render });
  },

  nextPage: function () {
    if (!this.collection.hasNext) {
      return;
    }
    this.url.add('page', ++this.currentPage);
    this.collection.url = this.url.url();
    this.collection.fetch({ success: this.renderPage });
  },

  render: function () {
    this.$el.empty();
    this.$el.append('<ul class="ac-timeline"></ul>');
    if (this.collection.length > 0) {
      this.collection.each(function (item) {
        this.renderItem(item);
      }, this);
      this.$spinner.appendTo(this.$el);
    } else {
      this.$el.append('<p class="alert alert-info">' + gettext("No activity yet") + '</p>');
    }
  },

  renderPage: function (collection, data) {
    _.each(data.results, function (item) {
      this.renderItem(item);
    }, this);
  },

  renderItem: function (item) {
    var view = new ActionView({ model: item });
    $(view.render().el)
      .appendTo(this.$el.find('.ac-timeline:last'));
    if (this.$el.find('.ac-timeline:last').find('.locBoxH').length >= 3) {
      this.$el.append('<ul class="ac-timeline"></ul>');
    }
  }
});

return ActionList;

});
