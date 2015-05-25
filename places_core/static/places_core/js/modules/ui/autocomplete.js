//
// autocomplete.js
// ===============

// Customized jQuery-ui autocomplete.

require(['jquery',
         'jqueryui'],

function ($) {

"use strict";

$.fn.simpleAutocomplete = function (options) {
  var defaults = {
    url: '/api-locations/autocomplete/',
    className: 'form-control'
  };
  options = $.extend(defaults, options);
  return $(this).each(function () {
    var $this = $(this);
    var $fake = $('<input type="text">');
    $this.hide();
    $fake.addClass(options.className)
      .insertAfter($this);
    $fake.autocomplete({
      minLength: 4,
      source: options.url,
      select: function (e, ui) {
        e.preventDefault();
        this.value = ui.item.label;
        $this.val(ui.item.value);
      }
    });
  });
};

$(document).ready(function () {
  $('.autocomplete-plholder').simpleAutocomplete();
});

});
