//
// collection.js
// =============

// Collection that handles comment list.
// It may be used also for subcomments.

define (['backbone'],

function (Backbone) {

"use strict";

var CommentCollection = Backbone.Collection.extend({

  currentPage: 1,

  parse: function (data) {
    this.hasNext = data.next !== null;
    this.nextUrl = data.next;
    return data.results;
  }
});

return CommentCollection;

});
