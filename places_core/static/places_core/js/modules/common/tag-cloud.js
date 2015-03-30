//
// tag-cloud.js
// ============

// Tag cloud.

require(['jquery'], function ($) {

"use strict";

$(document).ready(function () {
	var max_counter = 0,
    i = 0,
    min_counter, avg;

  $('.tags > ul > li').each(function () {
    // We gather counter values for each tag.
    var count = parseInt($(this).attr('data-counter'), 10);
    if (count > max_counter) {
      max_counter = count;
    }
    if (min_counter === undefined || count < min_counter) {
      min_counter = count;
    }
    i++;
  });

  $('.tags > ul > li').each(function () {
    // Another loop - we assign classes based
    // on the values previously collected
    var count = parseInt($(this).attr('data-counter'), 10);

    if (count <= max_counter / 5) {
      $(this).addClass('tag1');
    } else if (count <= max_counter / 4) {
      $(this).addClass('tag2');
    } else if (count <= max_counter / 3) {
      $(this).addClass('tag3');
    } else if (count <= max_counter / 2) {
      $(this).addClass('tag4');
    } else {
      $(this).addClass('tag5');
    }
  });
});

});
