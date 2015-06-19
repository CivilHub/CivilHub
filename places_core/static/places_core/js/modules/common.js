//
// common.js
// =========

// Simple common scripts, such as tooltips etc.

define(['jquery',
        'bootstrap',
        'jpaginate',
        'js/modules/locations/sublocations',
        'js/modules/common/toggle-menu',
        'js/modules/common/lang-selector',
        'js/modules/common/bookmarks',
        'js/modules/common/tour',
        'js/modules/common/tag-cloud',
        'js/modules/common/abuse-report',
        'js/modules/common/cookie-warning',
        'js/modules/common/cookie-invite',
        'js/modules/common/messages',
        'js/modules/common/follow-button',
        'js/modules/notifications/notifications',
        'js/modules/ui/widgets',
        'js/modules/ui/search-toggle',
        'js/modules/userspace/user-popup',
        'js/modules/userspace/modal-login',
        'js/modules/bouncy-navigation/main'],

function ($) {

"use strict";

// "Static" pagination
// ---------------------

$('.custom-static-pagination').pagination({
  visibleEntries: 13
});

// textarea increases the height
$.each($('textarea'), function() {
  var offset = this.offsetHeight - this.clientHeight;

  var resizeTextarea = function(el) {
    $(el).css('height', 'auto').css('height', el.scrollHeight + offset);
  };
  $(this).on('keyup input', function() { resizeTextarea(this); });
});

// Common simple scripts.
// -------------------------------------------------------------------------

// Cancel button for some forms which allow back one page.
$('.cancel-btn').on('click', function () {
  history.go(-1);
});

// Tooltips for elements shared among templates.
$('.navbar-avatar').tooltip({ placement: 'bottom' });
$('.custom-tooltip').tooltip();
$('.custom-tooltip-bottom').tooltip({
  placement: 'bottom'
});
$('.custom-tooltip-right').tooltip({
  placement: 'right'
});

// Scroll to top button
// -------------------------------------------------------------------------

$(document).ready(function () {

  var $scrollButton = $(document.createElement('a'));

  $scrollButton.attr({
    id: 'scrollToTop',
    href: '#top',
    name: gettext('Scroll to top')
  });

  $('.wrap').append($scrollButton);

  if ($(window).scrollTop() < 300)
  $scrollButton.hide();

  $scrollButton.click(function () {
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
  });

  $(window).scroll(function () {
    if ($(window).scrollTop() > 300) {
      $scrollButton.fadeIn('slow');
    } else {
      $scrollButton.fadeOut('slow');
    }
  });
});


// Google Analyitics functions
// -------------------------------------------------------------------------

// google analyitics follow/unfollow user
$(document).ready(function(){
  var civFollowBtn = $('.civ-follow-btn');
  civFollowBtn.click(function(){
      if (civFollowBtn.hasClass('btn-follow')) {
      window.ga('send', 'event', 'follow', 'click', 'follow-user');
    }
    else if (civFollowBtn.hasClass('btn-unfollow')) {
      window.ga('send', 'event', 'follow', 'click', 'unfollow-user');
    }
  })
});

// google analyitics follow/unfollow location
$(document).ready(function(){
  var locFllwBtn = $('.loc-fllw-btn');
  locFllwBtn.click(function(){
      if (locFllwBtn.hasClass('btn-follow-location')) {
      window.ga('send', 'event', 'follow', 'click', 'follow-location');
    }
    else if (locFllwBtn.hasClass('btn-unfollow-location')) {
      window.ga('send', 'event', 'follow', 'click', 'unfollow-location');
    }
  })
});


});


