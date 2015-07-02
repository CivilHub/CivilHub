//
// view.js
// =======

// View for single notification (single list item).

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/moment',
        'text!js/modules/notifications/templates/notify_entry.html'],

function ($, _, Backbone, moment, html) {

"use strict";

var NotifyView = Backbone.View.extend({
  template: _.template(html),
  tagName: 'li',
  className: "clearfix",
  render: function () {
    var params = this.model.toJSON();
    params.created_at = moment(params.created_at).fromNowOrNow();
    this.$el.html(this.template(params));
    if (this.model.get('is_new')) {
      this.$el.addClass('new');
    }
    return this;
  }
});

return NotifyView;

});
