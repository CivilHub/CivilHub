/*
 * userspace-login.js
 * ==================
 * 
 * Strona logowania do serwisu.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone"
    },
    
    shim: {
        
        jpaginate: {
            deps: ["jquery"]
        },
        
        bootstrap: {
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
        
        bootbox: {
            deps: ["bootstrap"],
            exports: "bootbox"
        }
    }
});

require(['jquery', 'js/modules/common'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
    
});