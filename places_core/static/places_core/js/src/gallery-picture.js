//
// gallery-picture.js
// ==================
// 
// Szczegółowy widok pojedynczego zdjęcia w galerii lokacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/comments/comments'],

  function ($) {
      
    "use strict"
    
    $(document).trigger('load');
      
  });
});