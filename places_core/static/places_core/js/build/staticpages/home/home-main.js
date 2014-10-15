//
// Homepage
// -----------------------------------------------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        async: 'includes/require/async',
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

//
// Logowanie przez Google+
// -----------------------------------------------------------------------------

var signInCallback = function (result) {
    if (result['error']) {
        console.log('An error happened:', result['error']);
    } else {
        $('#code').attr('value', result['code']);
        $('#at').attr('value', result['access_token']);
        $('#google-plus').submit();
    }
};

/* Executed when the APIs finish loading */
function render() {
    // Additional params including the callback, the rest of the params will
    // come from the page-level configuration.
    var additionalParams = {
        'scope': window.GOOGLE_DATA.scope,
        'clientid': window.GOOGLE_DATA.id,
        'accesstype': 'offline',
        'cookiepolicy': 'single_host_origin',
        'callback': 'signInCallback'
    };

    // Attach a click listener to a button to trigger the flow.
    var signinButton = document.getElementById('googleplus');
    signinButton.addEventListener('click', function() {
        gapi.auth.signIn(additionalParams); // Will use page level configuration
    });
}

require(['jquery',
         'bootstrap',
         'js/common',
         'js/ui/validate',
         'async!https://apis.google.com/js/plusone.js',
         'includes/google/client'],

function ($) {
    
    "use strict";
    
    $('#pl-register-form').registerFormValidator();
    
    $(document).trigger('load');
});