//
// news-list.js
// ============

// Lista wszystkich wpisów w sekcji "News" dla pojedynczej lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/ui/active-form'], 
           
  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});