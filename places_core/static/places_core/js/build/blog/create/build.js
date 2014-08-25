({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        ui: 'js/ui/ui',
        common: 'js/common',
        ckeditor: 'includes/ckeditor/ckeditor',
        dropzone: 'includes/dropzone/dropzone',
        jqueryui: 'includes/jquery-ui/jquery-ui'
        
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
        },
        
        ckeditor: {
            exports: 'CKEDITOR'
        },
        
        dropzone: {
            exports: 'Dropzone'
        },
        
        jqueryui: {
            deps: ['jquery']
        }
    },
    name: "js/build/blog/create/news-create-main",
    out: "news-create-built.js"
})