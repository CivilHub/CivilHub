//
// model.js
// ========

// Basic comment model.

define(['underscore',
        'backbone',
        'js/modules/utils/utils'],

function (_, Backbone, utils) {

"use strict";

function send(url, data, fn, context) {
  data.csrfmiddlewaretoken = utils.getCookie('csrftoken');
  $.post(url, data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

var CommentModel = Backbone.Model.extend({
  url: function () {
    var origUrl = Backbone.Model.prototype.url.call(this);
    origUrl += (origUrl.charAt(origUrl.length - 1) == '/' ? '' : '/');
    var res = (new RegExp(/\?parent\=[0-9]+/)).exec(origUrl);
    if (!_.isNull(res)) {
      origUrl = origUrl.replace(res[0] + '/', '');
    }
    return origUrl;
  },

  flag: function (vote) {
    var data = (!_.isUndefined(vote)) ? { vote: vote } : {};
    send(this.url() + 'moderate/', data, function (response) {
      this.set({
        is_removed: response.is_removed,
        reason: response.reason
      });
    }, this);
  }
});

return CommentModel;

});
