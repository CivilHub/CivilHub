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

function getStreamFilters ($el) {
  var filters = {};
  $el.each(function () {
    if ($(this).hasClass('active')) {
      filters[$(this).attr('data-control')] = $(this).attr('data-target');
    }
  });
  filters.haystack = $('#haystack').val();
  return filters;
}

$.fn.activityStream = function () {
  return $(this).each(function () {
    var $this = $(this);
    var list = new ActionList({
      mode: $this.attr('data-type'),
      ct: $this.attr('data-ct'),
      pk: $this.attr('data-pk')
    });
    function checkSrcrollPosition () {
      var ptr = ($(window).scrollTop() / $(document).height()) * 100;
      if (ptr > getMinimalPtr()) {
        list.nextPage();
        $(window).off('scroll', checkSrcrollPosition);
        setTimeout(function () {
          $(window).on('scroll', checkSrcrollPosition);
        }, 2000);
      }
    }
    $('.list-controller').on('click', function (e) {
      e.preventDefault();
      $('[data-control="' + $(this).attr('data-control') + '"]')
        .removeClass('active');
      $(this).addClass('active');
      list.filter(getStreamFilters($('.list-controller')));
    });
    $(window).on('scroll', checkSrcrollPosition);
    return this;
  });
};

$(document).ready(function () {
  $('.activity-stream').activityStream();
});

});
