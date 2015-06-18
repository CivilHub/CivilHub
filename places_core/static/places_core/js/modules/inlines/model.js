//
// model.js
// ========

// Basic comment model.

define(['underscore',
        'backbone',
        'js/modules/utils/utils'],

function (_, Backbone, utils) {

"use strict";

function send(url, fn, context) {
  var data = { csrfmiddlewaretoken: utils.getCookie('csrftoken') };
  $.post(url, data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

var CommentModel = Backbone.Model.extend({
  url: function () {
    var origUrl = Backbone.Model.prototype.url.call(this);
    return origUrl + (origUrl.charAt(origUrl.length - 1) == '/' ? '' : '/');
  },

  flag: function () {
    send(this.url() + 'moderate/', function (response) {
      this.set('is_removed', response.is_removed);
    }, this);
  }
});

return CommentModel;

});
