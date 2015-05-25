//
// location-details.js
// ===================

// Summary and activities page in a location

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/locations/background',
           'js/modules/hotbox',
           'js/modules/actstream'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
