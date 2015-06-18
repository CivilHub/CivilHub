//
// comment-summary.js
// ==================

// Scripts for page devoted only for comments.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/inlines/summary',
           'js/modules/common'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
