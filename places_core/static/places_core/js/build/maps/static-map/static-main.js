//
// Mapa statyczna - przedstawiamy tylko punkty powiązane z konkretnym obiektem
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootbox: 'includes/bootstrap/bootbox',
        leaflet: 'includes/leaflet/leaflet'
    },
    
    shim: {
        jqueryui: { deps: ['jquery'] },
        
        underscore: {
            deps: ['jquery'],
            exports: '_'
        },
        
        backbone: {
            deps: ['underscore'],
            exports: 'Backbone'
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        tagsinput: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'js/maps/map',
         'bootstrap',
         'js/common/bookmarks'],

function ($, CivilMap) {
    
    "use strict";
    
    // Main application controller
    
    var app = app || {};
    
    _.extend(app, {
        
        // Create main map application
        
        application: new CivilMap({
            elementID: 'main-map',
            mode: 'static',
            markers: window.CIVILAPP.markers,
            center: [window.CIVILAPP.position.lat, window.CIVILAPP.position.lng]
        }),
    });
    
    window.test = app.application;
    
    $(document).trigger('load');
    
});