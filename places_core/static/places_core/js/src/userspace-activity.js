//
// userspace-activity.js
// =====================
// 
// Podsumowanie aktywności związanej z obiektami śledzonymi przez użytkownika.
// E.g. dashboard.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/actstream/actions/actionList',
           'js/modules/content/content-list',
           'js/modules/common'],

  function($, ActionList) {
      
    "use strict";
    
    $('.col-sm-9.colHline').addClass('colHlineR');
    $('.col-sm-3.colHline').addClass('colHlineL');

    var actions = new ActionList();
    
    // Check if there is a better way to handle external events.
    $('.list-controller').on('click', function (e) {
      e.preventDefault();
      actions.filter($(this).attr('data-target'));
    });
    
    // Enable lazy-loading on page scrolling
    $(window).scroll(function() {
      if($(window).scrollTop() + $(window).height() == $(document).height()) {
        actions.getPage();
      }
    });
    
    $(document).trigger('load');
      
  });
});