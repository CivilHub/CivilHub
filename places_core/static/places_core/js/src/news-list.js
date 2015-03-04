//
// news-list.js
// ============
// 
// Lista wszystkich wpisów w sekcji "News" dla pojedynczej lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/blog/category-creator',
           'js/modules/blog/news-list/blog'], 
           
  function ($) {

    "use strict";

    $(document).trigger('load');
      
  });
});