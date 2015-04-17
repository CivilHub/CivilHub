//
// collection.js
// =============

// Simple model and collection for HotBox.

define(['backbone'],

function (Backbone) {

"use strict";

var HotBoxModel = Backbone.Model.extend({});

var HotBoxCollection = Backbone.Collection.extend({
  model: HotBoxModel
});

return HotBoxCollection;

});
