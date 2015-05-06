//
// actionCollection.js
// ===================

// Manage user actions.

define(['backbone',
        'js/modules/actstream/action-model'],

function (Backbone, ActionModel) {

"use strict";

var ActionCollection = Backbone.Collection.extend({
  model: ActionModel,
  parse: function (data) {
    this.hasNext = data.next !== null;
    this.nextUrl = data.next;
    return data.results;
  }
});

return ActionCollection;

});
