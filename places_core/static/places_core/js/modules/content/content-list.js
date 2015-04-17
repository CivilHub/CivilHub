//
// content-list.js
// ===============

// Scripts that support paginable list of entries. Made mainly
// with a summary of locations and the user site in mind.
//
// This script supports a full list of filters and lazy-loading.

require(['jquery',
         'js/modules/content/content-collection'],

function ($, ContentList) {

  "use strict";

  var contents = new ContentList();

  var filterTextContent = function () {
    var $field = $('#haystack'),
      txt = $field.val();

    if (_.isUndefined(txt) || txt.length <= 1) {
      return false;
    }

    return txt;
  };

  var filterListContent = function () {
    var $sel = $('.list-controller'),
      opts = {},
      optType = null,
      optValue = null,
      haystack = filterTextContent();

    $sel.each(function () {
      var $this = $(this);

      if ($this.hasClass('active')) {
        optType = $this.attr('data-control');
        optValue = $this.attr('data-target');
        opts[optType] = optValue;
      }
    });

    if (haystack !== false) {
      opts['haystack'] = haystack;
    }

    return opts;
  };

  function getMinimalPtr () {
    var h = $(document).height();
    if (h <= 5000) {
      return 50;
    } else if (h <= 10000) {
      return 60;
    } else {
      return 75;
    }
  }

  function checkSrcrollPosition () {
    var ptr = ($(window).scrollTop() / $(document).height()) * 100;
    if (ptr > getMinimalPtr()) {
      contents.getPage();
      $(window).off('scroll', checkSrcrollPosition);
      setTimeout(function () {
        $(window).on('scroll', checkSrcrollPosition);
      }, 2000);
    }
  }

  $(document).ready(function () {

    // Check if there is a better way to handle external events.

    $('#haystack-form').on('submit', function (e) {
      e.preventDefault();
      contents.filter(filterListContent());
    });

    $('.list-controller').on('click', function (e) {
      e.preventDefault();
      var selectedItem = $(this).attr('data-control');
      $('.active[data-control="' + selectedItem + '"]')
        .removeClass('active');
      $(this).addClass('active');
      contents.filter(filterListContent());
    });

    // Enable lazy-loading on page scrolling

    $(window).on('scroll', checkSrcrollPosition);
  });
});
