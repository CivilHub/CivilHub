//
// static-default.js
// =================
// 
// Domyślne skrypty stosowane dla wszystkich widoków w aplikacji
// "staticpages", które nie deklarują własnej konfiguracji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/utils/utils',
           'js/modules/common'],
           
  function ($) {
      
    "use strict";
    
    $(document).trigger('load');
      
  });
});