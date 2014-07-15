//
// config.js
// =========
//
// Require.js allows us to configure mappings to paths
// as demonstrated below:
require.config({
    baseUrl: '/static/places_core/',
    
    waitSeconds: 200,
    
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
        dropzone: 'includes/dropzone/dropzone',
        paginator: 'includes/backbone/backbone.paginator',
        moment: 'includes/momentjs/moment'
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
            deps: ['jquery']
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        'bootstrap-switch': {
            deps: ['bootstrap']
        },
        
        'bootstrap-fileinput': {
            deps: ['bootstrap']
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
        },
        
        moment: {
            exports: 'moment'
        }
    }
});

require(['js/main'], function () {
    $(document).trigger('load');
});