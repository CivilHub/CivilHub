//
// Homepage
// -----------------------------------------------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap'
    },
    
    shim: {
        bootstrap: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'bootstrap',
         'js/common/language'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
});