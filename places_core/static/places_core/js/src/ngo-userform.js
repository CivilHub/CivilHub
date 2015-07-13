//
// ngo-userform.js
// ===============

// Invite users to organization - scripts to handle forms.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/userspace/autocomplete'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
