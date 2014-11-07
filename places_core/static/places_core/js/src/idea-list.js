/*
 * idea-list.js
 * ============
 * 
 * Strona listy pomysłów w pojedynczej lokalizacji.
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
        paginator  : "includes/backbone/backbone.paginator",
        tagsinput  : "includes/jquery/jquery.tagsinput",
        bootbox    : "includes/bootstrap/bootbox",
        moment     : "includes/momentjs/moment"
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
    }
});

require(['jquery',
         'js/modules/common',
         'js/modules/locations/follow',
         'js/modules/ideas/idea-list/ideas',
         'js/modules/ideas/votes/votes',
         'js/modules/ideas/category-creator',
         'js/modules/inviter/userinviter'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
    
});