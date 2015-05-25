//
// view.js
// =======

// View for single notification (single list item).

define(['jquery',
        'underscore',
        'backbone',
        'text!js/modules/notifications/templates/notify_entry.html'],

function ($, _, Backbone, html) {

"use strict";

var NotifyView = Backbone.View.extend({
  template: _.template(html),
  tagName: 'li',
  className: "clearfix",
  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    if (this.model.get('is_new')) {
      this.$el.addClass('new');
    }
    return this;
  }
});

return NotifyView;

});
