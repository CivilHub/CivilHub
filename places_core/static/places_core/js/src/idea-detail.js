//
// idea-detail.js
// ==============
// 
// Szczegółowy widok pojedynczej idei.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/ideas/votes/votes',
           'js/modules/comments/comments',
           'js/modules/maps/pointer',
           'js/modules/inviter/userinviter',
           'js/modules/locations/follow'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});