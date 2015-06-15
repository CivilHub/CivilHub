//
// projects-default.js
// ===================

// Scripts that handle sites and forms connected with the project.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/progress',
           'js/modules/projects/tasks',
           'js/modules/inlines',
           'js/modules/common',
           'js/modules/common/counters'],

  function ($, ProgressForm) {
    "use strict";
    $(document).ready(function () {
      var form = new ProgressForm('checkbox-task');
    });
    $(document).trigger('load');
  });
});
