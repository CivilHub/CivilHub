//
// location-default.js
// ===================
// 
// Domyślne skrypty dla wszystkich podstron lokalizacji, które nie deklarują
// własnej konfiguracji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow'],

  function($) {
      
    "use strict";

    $(document).trigger('load');
      
  });
});