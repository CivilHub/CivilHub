//
// static-home.js
// ==============

// Show video on homepage and display register form errors in popups.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'bootstrap',
           'js/modules/common',
           'tubular'],
  function ($) {
    "use strict";
    $(document).ready(function () {
      // Show video in background
      if ($(window).width() >= 768 ) {
        $("#wrapper-Home").tubular({
          videoId: "H-q1wZcUHhk",
          mute: false,
          start: 29
        });
      }
      // Display registration form errors
      $('.error-popover').popover({
        placement: 'left'
      });
      $('.error-popover').popover('show');
    });
    $(document).trigger('load');
  });
});