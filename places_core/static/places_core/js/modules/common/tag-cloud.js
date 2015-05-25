//
// tag-cloud.js
// ============

// Tag cloud.

require(['jquery'], function ($) {

"use strict";

$(document).ready(function () {
  var i = 0;
  var maxCounter = 0;
  var avg;
  var minCounter;

  $('.tags > ul > li').each(function () {
    // We gather counter values for each tag.
    var count = parseInt($(this).attr('data-counter'), 10);
    if (count > maxCounter) {
      maxCounter = count;
    }
    if (minCounter === undefined || count < minCounter) {
      minCounter = count;
    }
    i++;
  });

  $('.tags > ul > li').each(function () {
    // Another loop - we assign classes based
    // on the values previously collected
    var count = parseInt($(this).attr('data-counter'), 10);

    if (count <= maxCounter / 5) {
      $(this).addClass('tag1');
    } else if (count <= maxCounter / 4) {
      $(this).addClass('tag2');
    } else if (count <= maxCounter / 3) {
      $(this).addClass('tag3');
    } else if (count <= maxCounter / 2) {
      $(this).addClass('tag4');
    } else {
      $(this).addClass('tag5');
    }
  });
});

});
