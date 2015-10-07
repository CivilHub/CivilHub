/**
 * form.js
 * =======
 *
 * Form to fill marker details, as well as show
 * some short summary and option buttons.
 */

define(['jquery',
        'underscore',
        'backbone',
        'bootbox'],

function ($, _, Backbone) {

"use strict";

function bConfirm (message, fn, context) {
  bootbox.confirm(message, function (response) {
    if (_.isFunction(fn)) fn.call(context, response);
  });
}

var MarkerForm = Backbone.View.extend({

  events: {
    'submit form': 'submit',
    'click .delete': 'deletePrompt'
  },

  render: function () {
    this.$('#label').val(this.model.get('label'));
    this.$('#description').val(this.model.get('description'));
    this.$('form').removeClass('hidden');
  },

  submit: function (e) {
    e.preventDefault();
    var data = {};
    _.each(this.$('form').serializeArray(), function (item) {
      data[item.name] = item.value;
    });
    this.model.set(data);
    this.model.save();
  },

  deletePrompt: function () {
    bConfirm(gettext("Are you sure?"), function (response) {
      if (response) this.model.destroy();
      this.$('form').addClass('hidden');
    }, this);
  }
});

return MarkerForm;

});

