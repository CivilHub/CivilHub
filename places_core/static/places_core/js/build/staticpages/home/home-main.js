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
        validate: 'js/ui/validate'
    },
    
    shim: {
        validate: {
            deps: ['jquery']
        },
        
        bootstrap: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'bootstrap',
         'validate',
         'js/common/language'],

function ($) {
    
    "use strict";
    
    $('#pl-register-form').registerFormValidator();
    
    $(document).trigger('load');
});