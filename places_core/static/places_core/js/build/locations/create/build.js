({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        'bootstrap-fileinput': 'includes/bootstrap/bootstrap.file-input',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        leaflet: 'includes/leaflet/leaflet'
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
        
        mapinput: {
            deps: ['jquery']
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        'bootstrap-fileinput': {
            deps: ['bootstrap']
        },
    },
    name: "js/build/locations/create/location-create-main",
    out: "location-create-built.js"
})