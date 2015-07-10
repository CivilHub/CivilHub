//
// user-ranking.js
// ===============

// User ranking table with searching and filtering.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/userspace/ranking'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
