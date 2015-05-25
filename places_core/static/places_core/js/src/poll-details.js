//
// poll-details.js
// ===============

// A detailed poll view - here we answer the question, if wwe still have
// that option available.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/common/counters',
           'js/modules/maps/pointer',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter'],

  function ($, Minimap) {
    "use strict";
    $(document).trigger('load');
  });
});
