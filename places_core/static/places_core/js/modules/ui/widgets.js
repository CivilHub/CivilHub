//
// widgets.js
// =============

// Zbiór widgetów łączący pluginy jQuery i inne widgety
// dopasowane do projektu lub utworzone z myślą o nim.

require(['jquery',
         'jqueryui',
         'js/modules/editor/plugins/uploader',
         'redactor',
         'bootstrap-switch',],

function ($) {

  "use strict";

  // Nakładka na jquery-ui.Datepicker, pozwalająca nam
  // odpowiednio formatować datę i zakładać widget
  // na podstawie klasy 'custom-datepicker' wykrytej
  // w atrybutach elementu.

  $.fn.customDatepicker = function (options) {
    return $(this).each(function () {
      $(this).datepicker({
        dateFormat: "yy-mm-dd"
      }).attr({
        'readonly': 'readonly'
      });
    });
  };

  $(document).ready(function () {
    $('.custom-datepicker').customDatepicker();
  });

  // Nakładka na edytor WYSIWYG Redaktor.

  // Opcja 'gallery' (true/false) plugin z galerią (domyślnie true).

  $.fn.customRedactor = function (options) {
    var settings = $.extend({'gallery': true}, options);
    return $(this).each(function () {
      var redactorSettings = {
        buttons: ['bold', 'italic', 'unorderedlist', 'orderedlist', 'link']
      };
      if (settings.gallery) {
        redactorSettings.plugins = ['uploader'];
      }
      $(this).redactor(redactorSettings);
    });
  };

  $(document).ready(function () {
    $('.custom-wysiwyg').customRedactor();
    $('.custom-wysiwyg-no-gallery').customRedactor({
      gallery: false
    });
  });

  // Zmieniamy checkboxy na bootstrap-swich. Należy zastosować
  // klasę 'custom-bs-switch' na elemencie.

  $(document).ready(function () {
    $('.custom-bs-switch').bootstrapSwitch({
      wrapperClass: 'form-group',
      onColor: 'success',
      offColor: 'danger'
    });
  })

});