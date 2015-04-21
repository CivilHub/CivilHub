//
// widgets.js
// =============

// A collection of widgets that connect jQuery plugins
// and other widgets that are suited for the project or
// were created with the application in mind.

require(['jquery',
         'jqueryui',
         'js/modules/editor/plugins/uploader',
         'redactor',
         'bootstrap-switch',
         'tagsinput'],

function ($) {

"use strict";

// A jquery-ui.Datepicker overlay that allows us to
// format the date correctly and to create a widget
// based on 'custom-datepicker' class detected in
// the attributed of the element.

$.fn.customDatepicker = function (options) {
  return $(this).each(function () {
    $(this).datepicker({
      dateFormat: "yy-mm-dd"
    }).attr({
      readonly: 'readonly'
    });
  });
};

$(document).ready(function () {
  $('.custom-datepicker').customDatepicker();
});

// A WYSIWYG Redaktor overlay

// The 'gallery' option (true/false) plugin along with the
// gallery (set to true by default)

$.fn.customRedactor = function (options) {
  var settings = $.extend({ gallery: true }, options);
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

// We change checkboxes into bootstrap-swich.
// 'custom-bs-switch' needs to be used on the element.

$(document).ready(function () {
  $('.custom-bs-switch').bootstrapSwitch({
    wrapperClass: 'form-group',
    onColor: 'success',
    offColor: 'danger'
  });
});

// Customized tagsinput for email address fields.

$.fn.emailInput = function () {
  return $(this).each(function () {
    var $input = $(this);
    var tagOptions = {
      defaultText: '',
      onPaste: true,
      onAddTag: function () {
        var oldValue = $input.val();
        var newValue = oldValue.replace(/ /g, ',');
        $input.importTags('');
        $input.importTags(newValue);
      }
    };
    if (!_.isUndefined($input.attr('data-autocomplete'))) {
      tagOptions.autocomplete_url = $input.attr('data-autocomplete');
    }
    $input.tagsInput(tagOptions);
  });
};

$(document).ready(function () {
  $('.email-input').emailInput();
});

$(document).ready(function () {
  var $input = $('<input type="text">');
  $input.addClass('form-control auto-fake-input');
  $('.autocomplete-plholder').hide().after($input);
});

});
