({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        ui: 'js/ui/ui',
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
        
        tagsinput: {
            deps: ['jquery']
        }
    },
    name: "js/build/gallery/media-form/media-form-main",
    out: "media-form-built.js"
})