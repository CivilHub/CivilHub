//
// visitors.js
// ===========

// Shows map with currently active visitors that we are able to track.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/visitors'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
