//
// Strona logowania użytkownika
//
//  => /templates/userspace/login.html
//
// -----------------------------------------------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap'
    },
    
    shim: {
        bootstrap: {
            deps: ['jquery']
        },
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
        //var token = gapi.auth.getToken();
        //window.test = token;
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

//
// Odpalamy skrypty
// -----------------------------------------------------------------------------

require(['jquery',
         'async!https://apis.google.com/js/plusone.js',
         'async!https://plus.google.com/js/client:plusone.js?onload=render',
         'js/common/language'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
    
});
