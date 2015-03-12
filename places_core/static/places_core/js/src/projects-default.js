//
// projects-default.js
// ===================

// Skrypty obsługujące strony i formularze powiązane z projektami.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/projects/tasks',
           'js/modules/comments/comments',
           'js/modules/common'],

  function($) {
    "use strict";
    $(document).trigger('load');
  });
});