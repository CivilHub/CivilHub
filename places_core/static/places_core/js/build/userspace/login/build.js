({
    baseUrl: "../../../../",
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone'
    },
    
    shim: {
        bootstrap: {
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
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        }
    },
    name: "js/build/userspace/login/userspace-login-main",
    out: "userspace-login-built.js"
})