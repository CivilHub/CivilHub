//
// collection.js
// =============

// Collection that handles comment list.
// It may be used also for subcomments.

define (['underscore',
         'backbone'],

function (_, Backbone) {

"use strict";

var CommentCollection = Backbone.Collection.extend({

  currentPage: 1,

  parse: function (data) {
    this.hasNext = data.next !== null;
    this.nextUrl = data.next;
    _.each(data.results, function (item) {
      console.log(item.id);
      console.log(this.get(item.id));
    }, this);
    return data.results;
  }
});

return CommentCollection;

});
