//
// default.js
// ==========
// 
// Domyślne skrypty stosowane kiedy widok nie deklaruje własnej konfiguracji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common'],
           
  function ($) {
      
    "use strict";
    
    $(document).trigger('load');
      
  });
});
