//
// location-create.js
// ==================

// New location creation

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/ui',
           'js/modules/locations/location-form',
           'js/modules/common'],

  function ($, ui) {
    "use strict";
    $(document).trigger('load');
  });
});
