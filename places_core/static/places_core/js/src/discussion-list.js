//
// discussion-list.js
// ==================

// A list of elements on the forum for a single location.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/ui/active-form'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
