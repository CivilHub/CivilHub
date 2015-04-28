//
// follow.js
// =========

// This is follow button ONLY for location objects. Necessary
// because of legacy methods related to Location model.

require(['jquery',
         'js/modules/utils/utils',
         'js/modules/ui/ui'],

function ($, utils, ui) {

"use strict";

var APIURL = '/api-locations/follow/?pk=';

function followRequest (pk, callback, context) {
  var token = utils.getCookie('csrftoken');
  $.post(APIURL + pk, { csrfmiddlewaretoken: token },
    function (response) {
      ui.message.success(response.message);
      callback.call(context, response);
    }
  );
}

function settext (following) {
  return following ? gettext("Stop following")
                   : gettext("Follow");
}

$(document).ready(function () {
  $('.loc-fllw-btn').on('click', function (e) {
    var id = $(this).attr('data-location-id');
    e.preventDefault();
    followRequest(id, function (response) {
      $(this).text(settext(response.following))
        .toggleClass('btn-follow-location')
        .toggleClass('btn-unfollow-location');
    }, this);
  });
});

});
