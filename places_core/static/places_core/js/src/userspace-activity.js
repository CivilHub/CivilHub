//
// userspace-activity.js
// =====================

// A summary of activities connected with objects followed by the user.
// E.g. dashboard.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/content/content-list',
           'js/modules/common',
           'js/modules/hotbox'],

  function ($, ActionList) {
    "use strict";
    $(document).trigger('load');
  });

});
