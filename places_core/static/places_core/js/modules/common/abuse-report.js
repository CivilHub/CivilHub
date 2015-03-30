//
// abuse-report.js
// ===============

// Allows users to send notifications about breaches
// in terms of use through a modal window

require(['jquery', 'js/modules/utils/abuse-window'],

function ($, AbuseWindow) {

"use strict";

$(document).ready(function () {

  var win = null, $link = null;

  $('.report-abuse-link').on('click', function (e) {
    e.preventDefault();
    $link = $(this);
    if (_.isNull(win)) {
      win = new AbuseWindow({
        'id': $link.attr('data-id') || 0,
        'content': $link.attr('data-content') || '',
        'label': $link.attr('data-label') || ''
      });
    }
    win.open();
  });
});

});
