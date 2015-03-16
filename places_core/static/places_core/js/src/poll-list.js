//
// poll-list.js
// ============

// Lista wszystkich ankiet utworzonych w ramach jednej lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/ui/active-form'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});