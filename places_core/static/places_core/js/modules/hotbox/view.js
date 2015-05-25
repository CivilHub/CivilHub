//
// view.js
// =======

// Main view for entire box.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/hotbox/entry',
        'text!js/modules/hotbox/templates/box.html'],

function ($, _, Backbone, HotBoxEntryView, html) {

"use strict";

var HotBox = Backbone.View.extend({

  template: _.template(html),

  initialize: function (options) {
    this.$el.html($(this.template(options)));
    this.$el.appendTo(options.appendTo);
    this.$list = this.$el.find('.ac-hot-box:first');
    this.$counter = this.$el.parent()
      .find('.ac-title > .badge-btn');
    _.bindAll(this, 'updateCounter');
    $.get(options.url, this.updateCounter);
  },

  updateCounter: function (data) {
    _.each(data, function (item) {
      this.renderItem(new Backbone.Model(item));
    }, this);
    this.$counter.text(data.length);
  },

  renderItem: function (item) {
    var view = new HotBoxEntryView({
      model: item
    });
    $(view.render().el)
      .appendTo(this.$list);
  }
});

return HotBox;

});
