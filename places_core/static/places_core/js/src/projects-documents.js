//
// projects-documents.js
// =====================

// Handles scripts related to project documents sub-pages.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/projects/document-form'],

  function($) {
    "use strict";
    $(document).trigger('load');
  });
});