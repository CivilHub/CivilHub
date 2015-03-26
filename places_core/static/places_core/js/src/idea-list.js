//
// idea-list.js
// ============

// A site with a list of ideas in a single location.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/ideas/votes/votes',
           'js/modules/inviter/userinviter',
           'js/modules/ui/active-form'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});