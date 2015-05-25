//
// autocomplete.js
// ===============

// Handles autocomplete for locations. We are replacing original inputs that
// takes list of comma-separated location ID's and provide autocomplete for
// such fields.

require(['jquery',
         'jqueryui'],

function ($) {

"use strict";

$.fn.lAutocomplete = function () {
  return $(this).each(function () {
    var $this = $(this);
    return this;
  });
};

$(document).ready(function () {
  $('.custom-l-autocomplete').lAutocomplete();
});

});
