//
// collection.js
// =============

// Collection that handles comment list.
// It may be used also for subcomments.

define (['underscore',
         'backbone',
         'js/modules/inlines/model'],

function (_, Backbone, CommentModel) {

"use strict";

var CommentCollection = Backbone.Collection.extend({

  model: CommentModel,

  currentPage: 1,

  parse: function (data) {
    this.hasNext = data.next !== null;
    this.nextUrl = data.next;
    return data.results;
  }
});

return CommentCollection;

});
