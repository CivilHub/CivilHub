//
// cookie-warning.js
// =================

// Wyświetlenie ostrzeżenia o cookie.

require(['jquery', 'js/modules/utils/utils'],

function ($, utils) {

"use strict";

function showCookieWarning () {
	$('#cookie-msg').prepend('<div class="alert fade in fade out">' + gettext('Cookies help us to deliver our services. By using our services, you agree to our use of cookies') + '.' + '<a class="btn" href="/cookies">' + gettext("Polityka cookies") + '</a><a id="accept-button" class="btn" data-dismiss="alert">OK</a></div>')
    .hide().fadeIn('slow');
  $('#accept-button').click(function () {
      utils.setCookie('cookie_msg', true, 365);
      $('#cookie-msg').fadeOut('slow', function() {
        $(this).empty().remove();
      });
  });
}

if(!utils.getCookie('cookie_msg') && !CivilApp.debug) {
	showCookieWarning();  
}

});
