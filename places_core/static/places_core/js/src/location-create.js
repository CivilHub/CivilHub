//
// location-create.js
// ==================
// 
// Tworzenie nowej lokacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/locations/location-form',
           'js/modules/common'],

  function ($, LocationForm) {
      
    "use strict";
    
    $(document).ready(function () {
      var form = new LocationForm();
    });
    
    $(document).trigger('load');
      
  });
});