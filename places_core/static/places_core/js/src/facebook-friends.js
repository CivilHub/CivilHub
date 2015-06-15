//
// facebook-friends.js
// ===================

// Scripts that allow registered users to fallow his/her FB friends.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/userspace/follow-all',
           'js/modules/common'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
