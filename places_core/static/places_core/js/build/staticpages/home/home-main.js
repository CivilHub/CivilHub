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
         'bootstrap'],

function ($) {
    
    "use strict";
    
    //~ $(document).ready(function () {
        //~ $('#pl-register-form').registerFormValidator();
    //~ });
    
    $(document).trigger('load');
});