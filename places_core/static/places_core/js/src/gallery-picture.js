//
// gallery-picture.js
// ==================

// A detailed view of a single image in the location's gallery

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/common/counters',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/comments/comments'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
