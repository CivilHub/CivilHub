//
// actionModel.js
// ==============

// Base model for all actions.

define(['backbone'],

function (Backbone) {

"use strict";

var ActionModel = Backbone.Model.extend({
  defaults: {
    description: ''
  },

  parse: function (model) {
    model.label = gettext("Write a comment");
    return model;
  }
});

return ActionModel;
});
