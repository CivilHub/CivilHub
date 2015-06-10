//
// poll-results.js
// ===============

// Single poll results review.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/polls/chartmaker',
           'js/modules/common',
           'js/modules/locations/follow'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
