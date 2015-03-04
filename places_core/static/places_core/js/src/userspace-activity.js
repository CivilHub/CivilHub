/*
 * userspace-activity.js
 * =====================
 * 
 * Podsumowanie aktywności związanej z obiektami śledzonymi przez użytkownika.
 * E.g. dashboard.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        bootstrap  : "includes/bootstrap/bootstrap",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        tagsinput  : "includes/jquery/jquery.tagsinput",
        bootbox    : "includes/bootstrap/bootbox",
        "tour": "includes/tour/bootstrap-tour",
        "moment": "includes/momentjs/moment"
    },
    
    shim: {
        
        jpaginate: {
            deps: ["jquery"]
        },
        
        underscore: {
            deps: ["jquery"],
            exports: "_"
        },
        
        backbone: {
            deps: ["underscore"],
            exports: "Backbone"
        },
        
        bootstrap: {
            deps: ["jquery"]
        },
        
        bootbox: {
            deps: ["bootstrap"],
            exports: "bootbox"
        },

        "tour": {
            "deps": ["bootstrap"]
        },
        
        tagsinput: {
            deps: ["jquery"]
        },
    }
});

require(['jquery',
         'js/modules/actstream/actions/actionList',
         'js/modules/content/content-list',
         'js/modules/common'],

function($, ActionList) {
    
    "use strict";
    
    $(document).ready(function(){
        $('.col-sm-3.colHline').addClass('colHlineL');
        $('.col-sm-9.colHline').addClass('colHlineR');
    });

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