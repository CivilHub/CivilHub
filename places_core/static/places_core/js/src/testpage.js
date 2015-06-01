//
// testpage.js
// ===========

// Te skrypty nie mają zastosowania na żadnej podstronie.
// Są tylko do testowania różnego stuffu.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'underscore',
           'js/modules/facebook',
           'js/modules/common'],

  function ($, _, CFBConnector) {
    "use strict";
    var conn = new CFBConnector();
    window.test = conn;
  });
});
