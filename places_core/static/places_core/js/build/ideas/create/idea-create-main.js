//
// Formularze tworzący nową ideę
//
//  => /templates/locations/location_idea_form.html
//
// ------------------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 400,
    
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
    }
});

require(['jquery',
         'jqueryui',
         'common',
         'js/editor/plugins/uploader',
         'js/locations/follow',
         'js/inviter/userinviter',
         'js/ideas/idea-form',
         'js/ideas/category-creator'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
    
});