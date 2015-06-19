//
// reason.js
// =========

// Show list of available options for comment moderator.

define(['jquery',
        'underscore',
        'backbone',
        'text!js/modules/inlines/templates/reason_form.html'],

function ($, _, Backbone, html) {

"use strict";

function fetch (fn, context) {
  $.get('/api-core/reasons/', function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

var ReasonForm = Backbone.View.extend({

  className: 'comment-reason-form',

  template: _.template(html),

  events: {
    'select change': 'onSelect'
  },

  initialize: function (options) {
    this.position = options.position;
    this.context = options.context || null;
    this.onSelect = options.onSelect || null;
    fetch(this.render, this);
  },

  render: function (data) {
    this.$el.attr('id', 'reason-form');
    this.$el.html(this.template({ options: data }));
    this.$el.appendTo('body');
    this.$form = this.$el.find('form:first');
    if (!_.isUndefined(this.position)) {
      this.$el.offset(this.position);
    }
    this.$el.on('click', function (e) {
      e.stopImmediatePropagation();
    });
    $(document).on('click', function (e) {
      this.destroy();
      $(document).off('click');
    }.bind(this));
    this.$form.on('submit', function (e) {
      e.preventDefault();
      this.handleSelect();
    }.bind(this));
  },

  handleSelect: function () {
    var $select = this.$('select:first');
    if (_.isFunction(this.onSelect)) {
      this.onSelect.call(this.context, $select.val());
    }
    this.destroy();
  },

  destroy: function () {
    this.$el.empty().remove();
  }
});

return ReasonForm;

});
