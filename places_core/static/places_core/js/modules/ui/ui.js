//
// ui.js
// -----
//
// Scripts related to user interface, such as flash
// messages, date pickers etc.

define(['jquery',
        'underscore',
        'backbone',
        'bootbox'],

function ($, _, Backbone, bootbox) {

"use strict";

var ui = ui || {};

//
// Flash messages framework.
// -------------------------------------------------------------------------

//
// Single message constructor.
// ---------------------------
ui.FlashMsg = Backbone.View.extend({
  tagName: 'div',

  className: 'alert',

  // The added templated for notifications is in places_core/templates

  template: _.template($('#flash-msg-tpl').html()),

  events: {
    mouseover: 'highlight'
  },

  render: function (msg, lvl) {
    var that = this;
    this.$el.html(this.template({ message: msg }));
    this.$el.addClass('alert-' + lvl + ' messageAlert ').fadeIn();
    this.setClock();
    return this;
  },

  setClock: function () {
    var that = this;
    this.clock = setTimeout(function () {
      that.remove.call(that);
    }, 5000);
  },

  highlight: function () {
    var that = this;
    this.$el.addClass('active');
    this.stopClock();
    this.$el.one('mouseout', function () {
      that.setClock();
      that.$el.removeClass('active');
    });
  },

  stopClock: function () {
    clearTimeout(this.clock);
  },

  remove: function () {
    var that = this;
    this.$el.fadeOut('slow', function () {
      that.$el.empty().remove();
    });
  }
});

// Represents entire messages area on screen.
// ------------------------------------------

ui.MessageArea = Backbone.View.extend({
  el: '#messages',

  addMessage: function (msg, lvl) {
    var view = new ui.FlashMsg();
    $(view.render(msg, lvl).el).appendTo(this.$el);
  },

  alert: function (msg) {
    this.addMessage(msg, 'danger');
  },

  warning: function (msg) {
    this.addMessage(msg, 'warning');
  },

  info: function (msg) {
    this.addMessage(msg, 'info');
  },

  success: function (msg) {
    this.addMessage(msg, 'success');
  }
});

// Handy interface for messages via ui object.
// --------------------------------------------

window.message = ui.message = new ui.MessageArea();

// Confirmation window
//
// Mostly used when users try to delete model, to avoid
// unintentional deletion. It is made to be used with bootbox
// confirm window.
//
// @param callback {function} Callback method
// @param context  {object}   Object, on which we want to act
// @param params   {void}     Additional params for function call
//
// @returns undefined

ui.confirmWindow = function (callback, context, params) {
  var msg = gettext("Are you sure you want to do this?");
  context = context || {};
  params = params || {};
  bootbox.confirm(msg, function (resp) {
    if (resp && typeof(callback) === 'function') {
      callback.apply(context, params);
    }
  });
};

return ui;

});
