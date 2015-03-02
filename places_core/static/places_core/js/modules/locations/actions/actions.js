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
  
  // Enable lazy-loading on page scrolling

  $(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() == $(document).height()) {
      actions.getPage();
    }
  });
});