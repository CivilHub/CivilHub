//
// location-background.js
// ======================

// Setting the background image for a location.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/image-form',
           'js/modules/common'],

  function ($, ImageForm) {

    "use strict";

    $(document).ready(function () {
      var form = new ImageForm({
        $el: $('#user-background-form'),
        orientation: 'landscape',
        maxWidth: 820
      });
    });

    $(document).trigger('load');

  });
});
