/*
 * gallery-picture.js
 * ==================
 * 
 * Szczegółowy widok pojedynczego zdjęcia w galerii lokacji.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        tagsinput  : "includes/jquery/jquery.tagsinput",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        paginator  : "includes/backbone/backbone.paginator",
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
        }
    }
});

require(['jquery',
         'js/modules/common',
         'js/modules/locations/follow',
         'js/modules/inviter/userinviter',
         'js/modules/comments/comments'],

function ($) {
    
    "use strict"
    
    $(document).trigger('load');
    
});