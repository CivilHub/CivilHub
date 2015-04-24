//
// userspace-profile.js
// ====================

// User profile that is available to see by other people.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/common/counters',
           'js/modules/userspace/enable-contacts',
           'js/modules/hotbox',
           'js/modules/actstream'],

  function ($) {
    "use strict";

    $('.list-controller').on('click', function (e) {
      e.preventDefault();
      var selectedItem = $(this).attr('data-control');
      $('.active[data-control="' + selectedItem + '"]')
        .removeClass('active');
      $(this).addClass('active');
    });

    $(document).trigger('load');
  });
});
