//
// Homepage
// -----------------------------------------------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
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
    }
});

require(['jquery',
         'bootstrap',
         'js/common',
         'js/ui/validate'],

function ($) {
    
    "use strict";
    
    $('#pl-register-form').registerFormValidator();
    
    $(document).trigger('load');
});