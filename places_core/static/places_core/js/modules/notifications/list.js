//
// list.js
// =======

// Basic view for entire list.

define(['jquery',
        'underscore',
        'backbone',
        'text!js/modules/notifications/templates/notify_list.html',
        'js/modules/utils/utils',
        'js/modules/notifications/config',
        'js/modules/notifications/collection',
        'js/modules/notifications/view'],

function ($, _, Backbone, html, utils, config, NotifyCollection, NotifyView) {

"use strict";

var defaults = {};

var NotifyList = Backbone.View.extend({

  template: _.template(html),

  initialize: function (options) {
    options = _.extend(defaults, options);
    this._opened = false;
    this.$parent = options.el || $('body');
    this.$indicator = this.$parent
      .find('.custom-badge-indicator:first');
    this.collection = new NotifyCollection();
    this.render();
    this.listenTo(this.collection, 'add', this.renderEntry);
  },

  initCollection: function () {
    var $link = this.$el.find('.more');
    this._container.empty();
    this.collection.fetch({
      success: function (collection) {
        if (collection.hasNext) {
          $link.show();
        }
      }
    });
  },

  render: function () {
    this.$el = $(this.template(null));
    this.$el.insertAfter(this.$parent);
    this._container = this.$el.find('ul:first');
    this.$el.find('.more').on('click', function () {
      this.nextPage();
    }.bind(this));
  },

  open: function () {
    if (this._opened) {
      return;
    }
    this.$el.fadeIn('fast', function () {
    this._opened = true;
      if (this.collection.length === 0) {
        this.initCollection();
      }
      $(document).one('click', function (e) {
        if ($(e.target).closest("#notifications-toggler")[0] ||
            $(e.target).closest(".more")[0]) {
          return;
        }
        this.close();
      }.bind(this));
    }.bind(this));
  },

  close: function () {
    if (!this._opened) {
      return;
    }
    this.$el.fadeOut('fast', function () {
      this._opened = false;
      this.markAll();
    }.bind(this));
  },

  toggle: function () {
    if (this._opened) {
      this.close();
    } else {
      this.open();
    }
  },

  renderEntry: function (item) {
    var notify = new NotifyView({
    model: item
    });
    $(notify.render().el)
      .appendTo(this._container);
  },

  markAll: function () {
    var $ind = this.$indicator;
    var data = {
      csrfmiddlewaretoken: utils.getCookie('csrftoken')
    };
    $.post('/api-notifications/mark/', data,
      function (response) {
        $ind.empty().remove();
      }
    );
  },

  nextPage: function () {
    var $link = this.$el.find('.more');
    if (!this.collection.hasNext) {
      return;
    }
    this.collection.url = [
      config.baseUrl, '?page=', ++this.collection.currentPage
    ].join('');
    this.collection.fetch({
      success: function (response) {
        if (!response.hasNext) {
          $link.hide();
        }
      }
    });
  }
});

return NotifyList;

});
