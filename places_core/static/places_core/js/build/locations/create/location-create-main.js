//
//

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox',
        dropzone: 'includes/dropzone/dropzone',
        mapinput: 'js/ui/jquery.mapinput',
        ckeditor: 'includes/ckeditor/ckeditor',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common',
        'async': 'includes/require/async',
        'bootstrap-fileinput': 'includes/bootstrap/bootstrap.file-input',
        'jqueryui': 'includes/jquery-ui/jquery-ui'
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
        
        dropzone: {
            exports: 'Dropzone'
        },
        
        ckeditor: {
            exports: 'CKEDITOR'
        },
        
        'bootstrap-fileinput': {
            deps: ['bootstrap']
        },
        
        'jquery-ui': {
            deps: ['jquery']
        }
    }
});

require(['jquery', 'js/locations/locationForm', 'common'], function ($, DiscussionForm) {
    
    var form = new DiscussionForm();
    
    $(document).trigger('load');
    
});