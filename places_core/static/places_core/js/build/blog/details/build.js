({
    baseUrl: "../../../../",
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        paginator: 'includes/backbone/backbone.paginator',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        moment: 'includes/momentjs/moment',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common',
        mapinput: 'js/ui/jquery.mapinput'
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
    name: "js/build/blog/details/news-details-main",
    out: "news-details-built.js"
})