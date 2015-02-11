({
    baseUrl: "../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        jpaginate: 'includes/jquery/jquery.paginate',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox',
        fullpagejs: 'includes/fullpagejs/jquery.fullPage'
    },
    
    shim: {
        
        jpaginate: {
            deps: ['jquery']
        },
        
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
        },

        fullpagejs: {
            deps: ['jquery']
        },
    },
    name: "js/src/features-page",
    out: "../dist/features-page.js"
})