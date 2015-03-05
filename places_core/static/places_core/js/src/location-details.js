//
// location-details.js
// ===================
// 
// Strona podsumowania i aktywności w lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/locations/actions/actions',
           'js/modules/content/content-list',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/locations/background'],

  function($) {

    "use strict";

    $('.col-sm-9.colHline').addClass('colHlineR');
    $('.col-sm-3.colHline').addClass('colHlineL');

    $(document).trigger('load');
      
  });
});