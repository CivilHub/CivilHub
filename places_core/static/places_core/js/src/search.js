//
// search.js
// =========

// Scripts for haystack search page - record, what users where searching for.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/search'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
