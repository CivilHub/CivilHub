//
// idea-list.js
// ============
// 
// Strona listy pomysłów w pojedynczej lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/ideas/idea-list/ideas',
           'js/modules/ideas/votes/votes',
           'js/modules/ideas/category-creator',
           'js/modules/inviter/userinviter'],

  function ($) {
      
    "use strict";

    $(document).trigger('load');
      
  });
});