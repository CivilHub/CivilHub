//
// default.js
// ==========

// Default scripts when the view does not declare its own configuration.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow'],

  function ($) {
    "use strict";
    $(document).ready(function () {
      $('#f-order-form select').on('change', function (e) {
        $(this).parents('form').submit();
      });
    });
    $(document).trigger('load');
  });
});
