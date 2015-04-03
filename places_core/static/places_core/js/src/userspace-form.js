//
// userspace-form.js
// =================
// 
// A form for user profile edition.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ui/image-form',
           'jqueryui',
           'js/modules/common'],

  function ($, ImageForm) {
      
    "use strict";
    
    $(document).ready(function () {
      var form = new ImageForm({
        $el: $('#upload-avatar-form'),
        orientation: 'portrait',
        maxWidth: 800
      });
    });

    $('#birth-date').attr("placeholder", "dd/mm/yyyy").datepicker({
      changeMonth: true,
      changeYear: true,
      minDate: new Date(1920, 1 - 1, 1),
      maxDate: 0,
      dateFormat: 'dd/mm/yy'
    });
    
    $('.simple-tabs-link').on('click', function (e) {
      e.preventDefault();
      var id = $(this).attr('data-target');
      if ($('#'+id).hasClass('active')) {
        return false;
      }
      $('.simple-tabs-tab').removeClass('active');
      $('#'+id).addClass('active');
    });
    
    $(document).trigger('load');
      
  });
});