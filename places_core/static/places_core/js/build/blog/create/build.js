({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        redactor: 'includes/redactor/redactor',
        dropzone: 'includes/dropzone/dropzone',
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
            deps: ['bootstrap']
        },
        
        jqueryui: {
            deps: ['jquery']
        },
        
        tagsinput: {
            deps: ['jqueryui']
        }
    },
    name: "js/build/blog/create/news-create-main",
    out: "news-create-built.js"
})