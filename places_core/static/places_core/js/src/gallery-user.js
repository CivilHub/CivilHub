//
// gallery-user.js
// ===============

// User gallery page

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/ui',
           'js/modules/common'],

  function ($, ui) {

    "use strict";

    function deletePicture(id) {
      $.ajaxSetup({
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
      });
      $.ajax({
        type: 'DELETE',
        url: '/api-gallery/usermedia/' + id + '/',
        success: function () {
          document.location.href = document.location.href;
        }
      });
    };

    $('.control-delete').on('click', function (e) {
      e.preventDefault();
      var id = $(this).attr('data-target');
      ui.confirmWindow(deletePicture, null, [id]);
    });

    $(document).trigger('load');
  });
});
