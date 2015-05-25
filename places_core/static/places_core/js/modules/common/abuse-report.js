//
// abuse-report.js
// ===============

// Allows users to send notifications about breaches
// in terms of use through a modal window

require(['jquery',
         'js/modules/utils/abuse-window'],

function ($, AbuseWindow) {

"use strict";

$(document).ready(function () {
  $('.abuse-link').on('click', function () {
    var win = new AbuseWindow(
      $(this).attr('data-ct'),
      $(this).attr('data-pk')
    );
  });
});

});
