/*
 * poll-details.js
 * ===============
 * 
 * Szczegółowy widok ankiety - tutaj odpowiadamy na pytanie, jeżeli mamy
 * jeszcze taką możliwość.
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
        tagsinput  : "includes/jquery/jquery.tagsinput",
        moment     : "includes/momentjs/moment",
        leaflet    : "includes/leaflet/leaflet"
    },
    
    shim: {
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
         'js/modules/maps/pointer',
         'js/modules/locations/follow',
         'js/modules/inviter/userinviter'],

function ($, Minimap) {
    
    "use strict";
    
    $(document).trigger('load');
    
});