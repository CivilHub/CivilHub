//
// notifications.js
// ================

// Entry point for entire notifications application.

define(['jquery',
        'js/modules/notifications/list'],

function ($, NotifyList) {

"use strict";

$(document).ready(function () {
  var list = new NotifyList({
    el: $('#notifications-toggler')
  });
  $('#notifications-toggler').on('click',
    function (e) {
      e.preventDefault();
      list.toggle();
    }
  );
});

});
