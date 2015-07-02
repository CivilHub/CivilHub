//
// voteCollection.js
// =================

// Model and collection for vote counter window.

define(['backbone'],

function (Backbone) {

"use strict";

var VoteModel = Backbone.Model.extend({});

var VoteCollection = Backbone.Collection.extend({
  model: VoteModel
});

return VoteCollection;

});
