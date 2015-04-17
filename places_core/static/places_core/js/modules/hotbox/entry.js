//
// entry.js
// ========

// Single entry in HotBox list.

define(['jquery',
        'underscore',
        'backbone',
        'text!js/modules/hotbox/templates/entry.html'],

function ($, _, Backbone, html) {

"use strict";

var HotBoxEntryView = Backbone.View.extend({

  className: 'ac-hot-single-box clearfix',

  template: _.template(html),

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    this.$el.find('.custom-tooltip-right')
      .tooltip({ placement: 'right' });
    return this;
  }
});

return HotBoxEntryView;

});
