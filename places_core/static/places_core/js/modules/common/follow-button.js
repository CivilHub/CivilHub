//
// follow-button.js
// ================

// This scripts cooperates with follow_button tag from activities app.

require(['jquery',
         'js/modules/utils/utils',
         'js/modules/ui/ui'],

function ($, utils, ui) {

"use strict";

var url = '/api-activities/follow/';

function sendData (url, data, callback, context) {
  $.post(url, data, function (response) {
    callback.call(context, response);
  });
}

function FollowButton (el) {
  var ct = $(el).attr('data-ct');
  var pk = $(el).attr('data-pk');
  this.$el = $(el);
  this.url = ([
    url, '?ct=', ct, '&pk=', pk
  ]).join('');
}

FollowButton.prototype.setTxt = function (following) {
  var txt = following ? gettext('Stop following')
                      : gettext('Follow');
  this.$el.text(txt);
};

FollowButton.prototype.toggle = function () {
  var data = { csrfmiddlewaretoken: utils.getCookie('csrftoken') };
  sendData(this.url, data, function (response) {
    if (response.success) {
      ui.message.success(response.message);
      this.setTxt(response.following);
      this.$el.toggleClass('btn-follow')
        .toggleClass('btn-unfollow');
    } else {
      ui.message.danger(response.message);
    }
  }, this);
};

$.fn.followButton = function () {
  return $(this).each(function () {
    var btn = new FollowButton(this);
    $(this).on('click', function (e) {
      e.preventDefault();
      btn.toggle();
    });
    return this;
  });
};

$(document).ready(function () {
  $('.civ-follow-btn').followButton();
});

});
