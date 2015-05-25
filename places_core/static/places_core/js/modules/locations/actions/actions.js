/**
 * actions.js
 * ==========
 *
 * Run app to manage user action stream.
 */
require(['jquery',
         'js/modules/actstream/actions/actionList'],

function ($, ActionList) {
    
  "use strict";
  
  var actions = new ActionList();

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
      actions.getPage();
      $(window).off('scroll', checkSrcrollPosition);
      setTimeout(function () {
        $(window).on('scroll', checkSrcrollPosition);
      }, 2000);
    }
  }
  
  // Enable lazy-loading on page scrolling

  $(window).on('scroll', checkSrcrollPosition);
});