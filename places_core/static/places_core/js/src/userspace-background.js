//
// userspace-background.js
// =======================

// Set background image for user profile.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/image-form',
           'js/modules/common'],

  function ($, ImageForm) {

    "use strict";

    $(document).ready(function () {
      var form = new ImageForm({
        $el: $('#user-background-form'),
        orientation: 'landscape'
      });
    });

    $(document).trigger('load');

  });
});
