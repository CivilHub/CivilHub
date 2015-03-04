//
// discussion-create.js
// ====================
// 
// Formularz do tworzenia/edycji tematów na forum.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'jqueryui',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/editor/plugins/uploader',
           'js/modules/inviter/userinviter',
           'js/modules/topics/discussion-form'],

  function ($) {
      
    "use strict";
    
    $(document).trigger('load');
      
  });
});