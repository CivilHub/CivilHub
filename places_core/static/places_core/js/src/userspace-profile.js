//
// userspace-profile.js
// ====================
// 
// Profil użytkownika udostępniony do przeglądania przez inne osoby.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/userspace/user-follow',
           'js/modules/common',
           'js/modules/userspace/actions/actions',
           'js/modules/userspace/enable-contacts'],

  function($) {

    "use strict";

    $(document).trigger('load');

  });
});