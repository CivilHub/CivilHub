//
// organization-detail.js
// ======================

// Activity stream for NGO.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/hotbox',
           'js/modules/actstream'],

  function ($, ActionList) {
    "use strict";
    $(document).trigger('load');
  });

});
