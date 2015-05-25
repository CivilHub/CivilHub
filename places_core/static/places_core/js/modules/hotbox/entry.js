//
// entry.js
// ========

// Single entry in HotBox list.

define(['jquery',
        'underscore',
        'backbone',
        'moment',
        'text!js/modules/hotbox/templates/entry.html'],

function ($, _, Backbone, moment, html) {

"use strict";

var HotBoxEntryView = Backbone.View.extend({

  className: 'ac-hot-single-box clearfix',

  template: _.template(html),

  render: function () {
    var context = this.model.toJSON();
    moment.locale(CivilApp.language);
    context.date_created = moment(context.date_created).fromNow();
    this.$el.html(this.template(context));
    this.$el.find('.custom-tooltip-right')
      .tooltip({ placement: 'right' });
    return this;
  }
});

return HotBoxEntryView;

});
