//
// discussion-list.js
// ==================
// 
// Lista tematów na forum dla pojedynczej lokalizacji.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/topics/category-creator',
           'js/modules/topics/discussion-list/discussions',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter'],

  function ($) {
      
    "use strict";

    $(document).trigger('load');
    
  });
});