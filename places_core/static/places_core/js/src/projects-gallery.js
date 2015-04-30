//
// projects-gallery.js
// ===================

// Image gallery for socialproject section.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/ui/run-lightbox'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
