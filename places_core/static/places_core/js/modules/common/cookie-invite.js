//
// cookie-invite.js
// =================

// Displays a cookie invite friends.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'text!tpl/cookie_if.html'],

function ($, _, utils, html) {

"use strict";

function showCookieInvite () {
  var nav = $("#navbar-top");

  if (utils.getCookie("cookie-if") && CivilApp.debug) {
    return;
  }

  $('#cookie-if').prepend(_.template(html), {})
    .hide().fadeIn('fast');
  $(nav).addClass('nav-cookie');
  $('body').addClass('body-cookie');
  $('.accept-btn-if').click(function () {
    $(nav).removeClass('nav-cookie');
    $('body').removeClass('body-cookie');
    utils.setCookie('cookie-if', true, 14);
    $('#cookie-if').fadeOut('fast', function () {
      $(this).empty().remove();
    });
  });
}

$(document).ready(function () {
  if (_.isNull(CivilApp.currentUserId) && CivilApp.debug) {
    return;
  } else {
    showCookieInvite();
  }
});

});
