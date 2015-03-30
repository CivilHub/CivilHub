//
// projects-default.js
// ===================

// Scripts that handle sites and forms connected with the project.

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