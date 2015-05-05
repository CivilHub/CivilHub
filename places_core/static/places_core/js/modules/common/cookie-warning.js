//
// cookie-warning.js
// =================

// Displays a cooky warning.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'text!tpl/cookie_msg.html'],

function ($, _, utils, html) {

"use strict";

function showCookieWarning () {
  if (utils.getCookie('cookie_msg') || CivilApp.debug) {
    return;
  }
  $('#cookie-msg').prepend(_.template(html), {})
    .hide().fadeIn('slow');
  $('#accept-button').click(function () {
    utils.setCookie('cookie_msg', true, 365);
    $('#cookie-msg').fadeOut('slow', function () {
      $(this).empty().remove();
    });
  });
}

$(document).ready(showCookieWarning);

});
