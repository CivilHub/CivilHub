//
// static-default.js
// =================
// 
// Default scripts used for all views in an "staticpages" application,
// that do not deklare their own configuration.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/utils/utils',
           'js/modules/common'],
           
  function ($) {
      
    "use strict";
    
    $(document).trigger('load');
      
  });
});