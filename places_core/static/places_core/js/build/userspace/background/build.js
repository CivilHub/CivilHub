({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox',
        color: 'includes/jquery/jquery.color',
        Jcrop: 'includes/jquery/jquery.Jcrop',
        'file-input': 'includes/bootstrap/bootstrap.file-input'
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
        
        color: {
            deps: ['jquery']
        },
        
        Jcrop: {
            deps: ['color']
        },
        
        'file-input': {
            deps: ['bootstrap']
        }
    },
    name: "js/build/userspace/background/userspace-background-main",
    out: "userspace-background-built.js"
})