//
// guide-details.js
// ================

// Detailed guide entry view.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/ui/scrollspy',
           'js/modules/comments/comments'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
