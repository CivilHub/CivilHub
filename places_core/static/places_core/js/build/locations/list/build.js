({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        vector: 'includes/vectormap/jquery-jvectormap-1.2.2.min',
        worldmap: 'includes/vectormap/jquery-jvectormap-world-mill-en',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common'
    },
    
    shim: {
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
        
        vector: {
            deps: ['jquery']
        },
        
        worldmap: {
            deps: ['vector']
        }
    },
    name: "js/build/locations/list/location-list-main",
    out: "location-list-built.js"
})