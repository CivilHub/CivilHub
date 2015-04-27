//
// organization-blog.js
// ====================

// Detailed page for NGO's blog articles.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/comments/comments'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
