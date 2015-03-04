//
// poll-details.js
// ===============
// 
// Szczegółowy widok ankiety - tutaj odpowiadamy na pytanie, jeżeli mamy
// jeszcze taką możliwość.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/maps/pointer',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter'],

  function ($, Minimap) {
      
    "use strict";
    
    $(document).trigger('load');
      
  });
});