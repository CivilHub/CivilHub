//
// search-toggle.js
// ================

// Toggle animation for search form in main navbar.

require(['jquery'], function ($) {

"use strict";

function toggleSearch ($box) {
  if ($box.hasClass('hidden')) {
    $box.removeClass('hidden')
      .animate({ width: "160px" }, 200);
  } else {
    $box.addClass('hidden')
      .animate({ width: "0px" }, 200);
  }
}

$(document).ready(function () {
  $('#search-bar-icon').on('click', function (e) {
    e.preventDefault();
    toggleSearch($('.search-bar-box'));
  });
});

});
