//
// votings-vote.js
// ===============

// Application part for front-end users, allowing them to vote for
// markers.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/mapvotes/vote-map',
           'js/modules/locations/follow'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
