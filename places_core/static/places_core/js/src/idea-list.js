//
// idea-list.js
// ============

// Strona listy pomysłów w pojedynczej lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/ideas/votes/votes',
           'js/modules/inviter/userinviter'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});