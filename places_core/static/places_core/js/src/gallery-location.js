//
// gallery-location.js
// ===================
//
// A gallery of a single location

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/ui',
           'js/modules/locations/follow',
           'js/modules/common'],

  function ($, ui) {
      
    "use strict";
    
    $('.control-delete').on('click', function (e) {
      e.preventDefault();
      var href = $(this).attr('href');
      ui.confirmWindow(function () {
        document.location.href = href;
      });
    });
    
    $(document).trigger('load');
  });
});