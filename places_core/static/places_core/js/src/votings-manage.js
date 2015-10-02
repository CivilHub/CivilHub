//
// votings.js
// ==========

// Module to vote for map markers related to projects.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/mapvotes/manage-map',
           'js/modules/locations/follow'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
