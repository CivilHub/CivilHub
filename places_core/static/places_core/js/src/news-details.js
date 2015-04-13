//
// news-details.js
// ===============

// A detailed article view in News location section

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/maps/pointer',
           'js/modules/comments/comments',
           'js/modules/inviter/userinviter',
           'js/modules/ui/run-lightbox'],

  function ($, Minimap) {
    "use strict";
    $(document).trigger('load');
  });
});
