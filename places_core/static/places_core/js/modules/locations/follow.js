//
// follow.js
// =========

// This is follow button ONLY for location objects. Necessary
// because of legacy methods related to Location model.

require(['jquery',
         'js/modules/utils/utils',
         'js/modules/ui/ui',
         'js/modules/locations/follow-button'],

function ($, utils, ui, fb) {

"use strict";

$(document).ready(function () {
  $('.loc-fllw-btn').on('click', function (e) {
    var id = $(this).attr('data-location-id');
    e.preventDefault();
    fb.followRequest(id, function (response) {
      $(this).text(fb.settext(response.following))
        .toggleClass('btn-follow-location')
        .toggleClass('btn-unfollow-location');
    }, this);
  });
});

});
