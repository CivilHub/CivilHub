//
// idea-detail.js
// ==============

// A detailed view of a single idea.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/common/counters',
           'js/modules/ideas/votes/votes',
           'js/modules/maps/pointer',
           'js/modules/inviter/userinviter',
           'js/modules/locations/follow',
           'js/modules/ui/run-lightbox',
           'js/modules/inlines'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
