//
// Activity stream dla użytkownika
//  => /templates/activity/actor.html
//

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox'
    },
    
    shim: {
        underscore: {
            deps: ['jquery'],
            exports: '_'
        },
        
        backbone: {
            deps: ['underscore'],
            exports: 'Backbone'
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        tagsinput: {
            deps: ['jquery']
        },
    }
});

require(['jquery',
         'js/actstream/actions/actionList',
         'js/common'],

function($, ActionList) {
    
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
    
    $(document).trigger('load');
    
});