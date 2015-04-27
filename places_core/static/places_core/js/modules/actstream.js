//
// actstream.js
// ============

// Handle activity streams.

require(['jquery',
         'js/modules/actstream/action-list'],

function ($, ActionList) {

"use strict";

function getMinimalPtr () {
  var h = $(document).height();
  if (h <= 5000) {
    return 10;
  } else if (h <= 10000) {
    return 30;
  } else {
    return 50;
  }
}

$.fn.activityStream = function () {
  return $(this).each(function () {
    var $this = $(this);
    var list = new ActionList({
      type: $this.attr('data-type'),
      ct: $this.attr('data-ct'),
      pk: $this.attr('data-pk')
    });
    function checkSrcrollPosition () {
      var ptr = ($(window).scrollTop() / $(document).height()) * 100;
      if (ptr > getMinimalPtr()) {
        list.getPage();
        $(window).off('scroll', checkSrcrollPosition);
        setTimeout(function () {
          $(window).on('scroll', checkSrcrollPosition);
        }, 2000);
      }
    }
    $(window).on('scroll', checkSrcrollPosition);
    return this;
  });
};

$(document).ready(function () {
  $('.activity-stream').activityStream();
});

});
