/*
 * poll-create.js
 * ==============
 * 
 * Interaktywny formularz do tworzenia ankiet.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        jqueryui   : "includes/jquery-ui/jquery-ui",
        tagsinput  : "includes/jquery/jquery.tagsinput",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone"
    },
    
    shim: {
        
        jpaginate: {
            deps: ["jquery"]
        },
        
        underscore: {
            deps: ["jquery"],
            exports: "_"
        },
        
        jqueryui: {
            deps: ["jquery"]
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
            deps: ["jqueryui"]
        }
    }
});

require(['jquery',
         'js/modules/common',
         'js/modules/locations/follow',
         'js/modules/inviter/userinviter',
         'js/modules/polls/poll-form/create-poll'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
    
});