({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox'
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
        }
    },
    name: "js/build/gallery/user-gallery/user-gallery-main",
    out: "user-gallery-built.js"
})