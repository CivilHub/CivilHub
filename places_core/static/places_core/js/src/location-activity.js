//
// location-details.js
// ===================

// Strona podsumowania i aktywności w lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/locations/actions/actions',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/locations/background'],

  function($) {
    "use strict";
    $(document).trigger('load');
  });
});