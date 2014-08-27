({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        paginator: 'includes/backbone/backbone.paginator',
        moment: 'includes/momentjs/moment',
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
        
        tagsinput: {
            deps: ['jquery']
        }
    },
    name: "js/build/gallery/picture-view/picture-view-main",
    out: "picture-view-built.js"
})