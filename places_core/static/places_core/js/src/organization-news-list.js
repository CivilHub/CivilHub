//
// organization-news-list.js
// ==========

// News list page for NGO.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/ui/run-lightbox'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
