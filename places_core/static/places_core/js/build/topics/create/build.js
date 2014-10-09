({
    baseUrl: "../../../../",
    paths: {
        jquery: 'includes/jquery/jquery',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        'bootstrap-switch': 'includes/bootstrap/bootstrap-switch',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        redactor: 'includes/redactor/redactor',
        dropzone: 'includes/dropzone/dropzone',
        leaflet: 'includes/leaflet/leaflet'
    },
    
    shim: {
        
        jqueryui: {
            deps: ['jquery']
        },
        
        tagsinput: {
            deps: ['jqueryui']
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
        
        'bootstrap-switch': {
            deps: ['bootstrap']
        },
        
        mapinput: {
            deps: ['jquery']
        }
    },
    name: "js/build/topics/create/discussion-create-main",
    out: "discussion-create-built.js"
})