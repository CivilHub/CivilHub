({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        fileinput: 'includes/bootstrap/bootstrap.file-input'
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
        
        fileinput: {
            deps: ['bootstrap']
        },
        
        tagsinput: {
            deps: ['jquery']
        },
    },
    name: "js/build/locations/details/location-details-main",
    out: "location-details-built.js"
})