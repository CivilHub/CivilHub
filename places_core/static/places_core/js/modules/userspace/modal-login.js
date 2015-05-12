//
// modal-login.js
// ==============

// This script presents login form in handy modal window. It will also fill
// in next parameter with current page url to redirect user after login complete.

require(['jquery',
         'underscore',
         'backbone',
         'bootstrap'],

function ($, _, Backbone) {

"use strict";

var ModalLogin = Backbone.View.extend({

  opened: false,

  initialize: function ($el) {
    this.$el = $el;
    this.$el.modal({ show: false });
    _.bindAll(this, '_open');
    _.bindAll(this, '_close');
    this.$el.on('shown.bs.modal', this._open);
    this.$el.on('hidden.bs.modal', this._close);
    this.$el.find('[type="submit"]').on('click', function (e) {
      this.$el.find('form').submit();
    }.bind(this));
  },

  toggle: function () {
    if (this.opened) {
      this.$el.modal('hide');
    } else {
      this.$el.modal('show');
    }
  },

  _open: function () {
    this.opened = true;
  },

  _close: function () {
    this.opened = false;
  }

});

$(document).ready(function () {
  if (!_.isNull(CivilApp.currentUserId)) {
    return;
  }
  var form = new ModalLogin($('#login-modal'));
  $('.civil-login-required').on('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    form.toggle();
  });
});

});
