//
// view.js
// =======

// Main view for entire box.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/hotbox/entry',
        'js/modules/hotbox/collection',
        'text!js/modules/hotbox/templates/box.html'],

function ($, _, Backbone, HotBoxEntryView, HotBoxCollection, html) {

"use strict";

var HotBox = Backbone.View.extend({

  template: _.template(html),

  initialize: function (options) {
    this.$el.html($(this.template(options)));
    this.$el.appendTo(options.appendTo);
    this.$list = this.$el.find('.ac-hot-box:first');
    this.$counter = this.$el.find('.ac-title > .badge-btn');
    this.collection = new HotBoxCollection();
    this.collection.url = options.url;
    this.listenTo(this.collection, 'add', this.renderItem);
    _.bindAll(this, 'updateCounter');
    this.collection.fetch({ success: this.updateCounter });
  },

  updateCounter: function (collection) {
    this.$counter.text(collection.length);
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
