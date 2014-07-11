//
// config.js
// =========
//
// Require.js allows us to configure mappings to paths
// as demonstrated below:
require.config({
    baseUrl: '/static/places_core/',
    
    paths: {
        jquery: 'includes/jquery/jquery',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        text: 'includes/require/text',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        bootstrap: 'includes/bootstrap/bootstrap',
        'bootstrap-switch': 'includes/bootstrap/bootstrap-switch',
        'bootstrap-fileinput': 'includes/bootstrap/bootstrap.file-input',
        bootbox: 'includes/bootstrap/bootbox',
        ckeditor: 'includes/ckeditor/ckeditor',
        dropzone: 'includes/dropzone/dropzone'
        
    },
    
    shim: {
        underscore: {
            exports: '_'
        },
        
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        
        jqueryui: {
            dep: ['jquery']
        },
        
        bootstrap: {
            deps: ['jquery'],
            exports: '$'
        },
        
        'bootstrap-switch': {
            deps: ['bootstrap'],
            exports: '$.fn.bootstrapSwitch'
        },
        
        'bootstrap-fileinput': {
            deps: ['bootstrap'],
            exports: '$.fn.bootstrapFileInput'
        },
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        ckeditor: {
            exports: 'CKEDITOR'
        },
        
        dropzone: {
            deps: ['jquery'],
            exports: 'Dropzone'
        }
    }
});

require(['bootstrap'], function ($) {
    
});