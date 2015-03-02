/*
 * gallery-location.js
 * ===================
 * 
 * Galeria pojedynczej lokalizacji.
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
        bootbox    : "includes/bootstrap/bootbox"
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
        }
    }
});

require(['jquery',
         'js/modules/ui/ui',
         'js/modules/locations/follow',
         'js/modules/common'],

function ($, ui) {
    
    "use strict";
    
    $('.control-delete').on('click', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        ui.confirmWindow(function () {
            document.location.href = href;
        });
    });
    
    $(document).trigger('load');
});