//
// actionList.js
// =============

// Entire action list view.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/actstream/action-collection',
        'js/modules/actstream/action-view',
        'jpaginate'],

function ($, _, Backbone, ActionCollection, ActionView) {

"use strict";

var apiUrl  = window.API_URL;

var apiUser = window.USER_ID;

var ActionList = Backbone.View.extend({

  el: '.activity-stream',

  nextPage: null,

  filterContent: false,

  mode: 'user',

  ct: null,

  pk: null,

  initCollection: function (callback, context, data) {
    $.get(apiUrl, data || {}, function (resp) {
      if (typeof(callback) === 'function') {
        callback.call(context, resp.results, resp.next);
      }
    });
  },

  initialize: function (options) {
    apiUrl = ([
      '/api-activities/actstream/',
      '?type=', options.type, '&ct=', options.ct,
      '&pk=', options.pk
    ]).join('');
    this.$spinner = $(document.createElement('span'));
    this.$spinner
      .addClass('fa fa-spin fa-circle-o-notch')
      .hide();
    this.initCollection(function (actions, next) {
      this.setPage(next);
      this.collection = new ActionCollection(actions);
      this.render();
      this.listenTo(this.collection, 'add', this.renderItem);
    }, this, { pk: apiUser });
  },

  filter: function (content) {
    this.filterContent = content || false;
    var data = {};
    data.pk = apiUser;
    if (this.filterContent) data.content = this.filterContent;
    this.initCollection(function (actions, next) {
      this.setPage(next);
      this.collection.reset(actions);
      this.render();
    }, this, data);
  },

  setPage: function (next) {
    if (next) {
      this.nextPage = parseInt(next.slice(next.indexOf('&page') + 6), 10);
    } else {
      this.nextPage = null;
    }
  },

  getPage: function (page) {
    page = page || this.nextPage;
    if (_.isNull(page)) return false;
    this.$spinner.appendTo(this.$el).fadeIn('fast');
    var data = {
      page: this.nextPage
    };
    if (this.filterContent) {
      data.content = this.filterContent;
    }
    this.initCollection(function (actions, next) {
      this.setPage(next);
      _.each(actions, function (item) {
        this.collection.add(item);
      }, this);
      this.$spinner.fadeOut('fast');
    }, this, data);
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

  renderItem: function (item) {
    var view = new ActionView({
      model: item
    });
    $(view.render().el)
      .appendTo(this.$el.find('.ac-timeline:last'));
    if (this.$el.find('.ac-timeline:last').find('.locBoxH').length >= 3) {
      this.$el.append('<ul class="ac-timeline"></ul>');
    }
  }
});

return ActionList;

});
