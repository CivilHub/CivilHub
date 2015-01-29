/**
 * content-list.js
 *
 * Skrypty obsługujące listę wpisów w głównym widoku lokalizaji.
 */
require(['jquery',
         'js/modules/locations/content/content-collection'],

function ($, ActionList) {

  "use strict";

  var contents = new ActionList();

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

  // Check if there is a better way to handle external events.

  $('.list-controller').on('click', function (e) {
    e.preventDefault();
    var selectedItem = $(this).attr('data-control');
    $('.active[data-control="' + selectedItem + '"]')
      .removeClass('active');
    $(this).addClass('active');
    contents.filter(filterListContent());
  });

  // Enable lazy-loading on page scrolling

  $(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() == $(document).height()) {
      contents.getPage();
    }
  });

  $('#haystack-form').bind('submit', function (e) {
    e.preventDefault();
    contents.filter(filterListContent());
  });

});