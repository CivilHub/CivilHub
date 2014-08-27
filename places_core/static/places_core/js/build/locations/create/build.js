({
    baseUrl: "../../../../",
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        'bootstrap-fileinput': 'includes/bootstrap/bootstrap.file-input',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        mapinput: 'js/ui/jquery.mapinput',
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