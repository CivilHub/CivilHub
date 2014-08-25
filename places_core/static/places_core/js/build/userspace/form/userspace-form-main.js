//
//
//

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 300,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        common: 'js/common',
        ckeditor: 'includes/ckeditor/ckeditor',
        dropzone: 'includes/dropzone/dropzone',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        utils: 'js/utils/utils',
        liquid: 'includes/jquery/imgLiquid'
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
        
        ckeditor: {
            exports: 'CKEDITOR'
        },
        
        jqueryui: {
            deps: ['jquery']
        },
        
        dropzone: {
            deps: ['jquery'],
            exports: 'Dropzone'
        },
        
        liquid: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'js/userspace/profile/profileForm',
         'common'],

function ($) {
    "use strict";
    
    $('#id_avatar').on('change', function (e) {
        $('#upload-avatar-form').submit();
    });
    
    $(document).trigger('load');
    
});