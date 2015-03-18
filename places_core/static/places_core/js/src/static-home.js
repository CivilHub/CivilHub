//
// static-home.js
// ==============
// 
// Strona domowa i formularz rejestracji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'bootstrap',
           'js/modules/common',
           'js/modules/ui/validate',
           'tubular'],

  function ($) {
      
    "use strict";
    
    if($(window).width() > 768 ){
      $("#wrapper-Home").tubular({
        videoId: "H-q1wZcUHhk",
        mute: false,
        start: 29
      });
    }

    $('#pl-register-form').registerFormValidator();
    
    $(document).trigger('load');

  });
});