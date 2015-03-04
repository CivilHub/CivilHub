//
// news-create.js
// ==============
// 
// Tworzenie/edycja wpisów w sekcji News lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'jqueryui',
           'js/modules/common',
           'js/modules/editor/plugins/uploader',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/blog/news-form'],

  function ($) {
      
    "use strict";
    
    $(document).trigger('load');
      
  });
});