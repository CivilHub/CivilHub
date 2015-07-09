//
// ranking.js
// ==========

// Ranking table for users - searching and filtering.

require(['jquery',
         'underscore'],

function ($, _) {

"use strict";

// Split URL GET params into object and highlight proper links.
//
// This function also takes care of filling search form input and
// append desc/asc order switch to control links.

function fillFormFromParams () {
  var getData = document.location.href.split('?');
  var params = {};

  // No GET params - nothing to do

  if (getData.length === 1) {
    return;
  }

  // Split params into JavaScript object

  _.each(getData[1].split('&'), function (param) {
    var tmp = param.split('=');
    params[tmp[0].trim()] = tmp[1].trim();
  });

  // Fill current link and adjust it's URL for asc and desc order.

  if (!_.isUndefined(params.o)) {
    var $el = $('[data-field="' + params.o + '"]');
    var href = $el.attr('href');
    $el.addClass('active');
    if (!_.isUndefined(params.d) && params.d === 'asc') {
      $el.addClass('link-asc');
      adjustUrl($el, 'desc');
    } else {
      $el.addClass('link-desc');
      adjustUrl($el, 'asc');
    }
  }

  // Fill initial search term into text input

  if (!_.isUndefined(params.q)) {
    $('#ranking-filter').val(params.q);
  }
}

// Set proper element url based on GET request made by user.
//
// This function checks for order parameter in href and either add it
// or replace if there already is one.
//
// @param { jQuery DOM Element }    Target link (usually 'a' element)
// @param { String }                Order as regular string (asc|desc)

function adjustUrl ($el, order) {
  order = order || 'desc';
  var href = $el.attr('href');
  var result = href.match(/d=([\w]+)/g);
  if (_.isNull(result)) {
    $el.attr('href', href + '&d=' + order);
    return;
  }
  $el.attr('href', href.replace(result, 'd=' + order));
}

// Run!

$(document).ready(fillFormFromParams);

});
