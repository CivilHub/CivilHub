/**
 * model.js
 * ========
 *
 * Model for marker that provides method such as ``vote``.
 */

define(['backbone',
        'js/modules/utils/utils'],

function (Backbone, utils) {

"use strict";

var MarkerModel = Backbone.Model.extend({

  url: function () {
    var origUrl = Backbone.Model.prototype.url.call(this);
    origUrl += (origUrl.charAt(origUrl.length - 1) == '/' ? '' : '/');
    return origUrl;
  },

  vote: function () {
    utils.sendData(this.url() + 'vote/', null, function (response) {
      if (response.success) {
        this.set('user_vote', response.status);
        this.trigger('voted', response.status);
      } else {
        this.trigger('voteError', response.error);
      }
    }, this);
  }
});

return MarkerModel;

});

