//
// abuse-report.js
// ===============

// Pozwala użytkownikom wysyłać powiadomienia o naruszeniu
// regulaminu przy pomocy modalowego okienka.

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
