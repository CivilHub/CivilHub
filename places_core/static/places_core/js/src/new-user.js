//
// default.js
// ==========

// Default scripts when the view does not declare its own configuration.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/simple-autocomplete'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
