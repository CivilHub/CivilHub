/*
 * location-create.js
 * ==================
 * 
 * Tworzenie nowej lokacji.
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
        backbone   : "includes/backbone/backbone",
        leaflet    : "includes/leaflet/leaflet",
        "bootstrap-fileinput": "includes/bootstrap/bootstrap.file-input"
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
        
        mapinput: {
            deps: ["jquery"]
        },
        
        bootstrap: {
            deps: ["jquery"]
        },
        
        bootbox: {
            deps: ["bootstrap"],
            exports: "bootbox"
        },
        
        "bootstrap-fileinput": {
            deps: ["bootstrap"]
        },
    }
});

require(['jquery',
         'js/modules/locations/location-form',
         'js/modules/common'],

function ($, LocationForm) {
    
    "use strict";
    
    $(document).ready(function () {
        var form = new LocationForm();
    });
    
    $(document).trigger('load');
    
});