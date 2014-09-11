//
// actions.js
// ==========
//
// Run app to manage user action stream.
//
require(['jquery',
         'js/actstream/actions/actionList'],

function ($, ActionList) {
    
    "use strict";
    
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
});