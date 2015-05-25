//
// model.js
// ========

// Basic comment model.

define(['backbone'],

function (Backbone) {

"use strict";

var CommentModel = Backbone.Model.extend({
  url: function () {
    var origUrl = Backbone.Model.prototype.url.call(this);
    return origUrl + (origUrl.charAt(origUrl.length - 1) == '/' ? '' : '/');
  }
});

return CommentModel;

});
