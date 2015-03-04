//
// location-background.js
// ======================
// 
// Ustawianie zdjęcia tła dla lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/image-form',
           'js/modules/common'],

  function($, ImageForm) {
      
    "use strict";
    
    $(document).ready(function () {
      var form = new ImageForm({
        $el: $('#user-background-form'),
        orientation: 'landscape'
      });
      window.test = form;
    });
    
    $(document).trigger('load');
      
  });
});