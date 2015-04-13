//
// idea-create.js
// ==============

// A form for creation/edition of ideas.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/ideas/idea-form'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
