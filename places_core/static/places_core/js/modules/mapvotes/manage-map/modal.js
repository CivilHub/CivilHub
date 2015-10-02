/**
 * modal.js
 * ========
 *
 * Triggered when user add new marker.
 */

define(['jquery',
        'underscore',
        'backbone',
        'bootstrap'],

function ($, _, Backbone) {

"use strict";

var ModalForm = Backbone.View.extend({

  events: {
    'click .submit': 'submit'
  },

  initialize: function (options) {
    this.collection = options.collection;
    this.$el.modal({show: false});
    this.$el.on('hidden.bs.modal', this.cleanup.bind(this));
    return this;
  },

  open: function (position) {
    this.$('[name="lat"]').val(position.lat);
    this.$('[name="lng"]').val(position.lng);
    this.$el.modal('show');
  },

  close: function () {
    this.$el.modal('hide');
  },

  getData: function () {
    var data = {};
    _.each(this.$('form').serializeArray(), function (item) {
      data[item.name] = item.value;
    }, this);
    data.voting = VA__MAP_DATA.voting;
    return data;
  },

  submit: function (e) {
    e.preventDefault();
    var self = this;
    var obj = this.collection.create(this.getData(), {
      error: function (model, response) {
        self.displayErrors(response.responseJSON);
      },
      success: function (model) {
        self.trigger('submit', model);
        self.close();
      }
    });
  },

  displayErrors: function (errors) {
    var $err = $('<p class="alert alert-danger"></p>');
    $err.text(errors.label);
    $err.prependTo(this.$('#va__label-group'));
    this.$('#va__label-group').addClass('has-error');
  },

  cleanup: function () {
    this.$('input, textarea').val('');
    this.$('#va__label-group').removeClass('has-error');
    this.$('.alert-danger').empty().remove();
  }
});

return ModalForm;

});

