//
// location-statistics.js
// ======================

// Different charts with location statistics.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/stats',
           'js/modules/locations/follow',
           'js/modules/locations/background'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
