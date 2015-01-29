/*
 * location-details.js
 * ===================
 * 
 * Strona podsumowania i aktywności w lokalizacji.
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
        tagsinput  : "includes/jquery/jquery.tagsinput",
        fileinput  : "includes/bootstrap/bootstrap.file-input"
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
        
        fileinput: {
            deps: ["bootstrap"]
        },
        
        tagsinput: {
            deps: ["jquery"]
        },
    }
});

require(['jquery',
         'js/modules/locations/actions/actions',
         'js/modules/content/content-list',
         'js/modules/common',
         'js/modules/locations/follow',
         'js/modules/inviter/userinviter',
         'js/modules/locations/background'],

function($) {
    
    "use strict";

    $(document).trigger('load');
    
});