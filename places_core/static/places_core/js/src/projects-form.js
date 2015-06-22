//
// projects-default.js
// ===================

// Scripts that handle sites and forms connected with the projects.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/projects/tasks',
           'js/modules/inlines',
           'js/modules/content/content-form',
           'js/modules/common'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
