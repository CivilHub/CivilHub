//
// blog-details.js
// ===============

// Detailed view of single aticles blog page.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/comments/comments'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
