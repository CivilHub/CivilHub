/*
 * news-list.js
 * ============
 * 
 * Lista wszystkich wpisów w sekcji "News" dla pojedynczej lokalizacji.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        paginator  : "includes/backbone/backbone.paginator",
        tagsinput  : "includes/jquery/jquery.tagsinput",
        moment     : "includes/momentjs/moment",
        tour       : "includes/tour/bootstrap-tour"
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
        
        tagsinput: {
            deps: ["jquery"]
        },

        tour: {
            deps: ["jquery"]
        },
    }
});

require(['jquery',
         'js/modules/common',
         'js/modules/locations/follow',
         'js/modules/inviter/userinviter',
         'js/modules/blog/category-creator',
         'js/modules/blog/news-list/blog'], 
         
function ($) {

    "use strict";

    $(document).trigger('load');
    
});