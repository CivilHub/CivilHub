//
// news-list.js
// ============

// A list of all entries in "News" section for a single location

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/ui/active-form',
           'js/modules/ui/run-lightbox'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
