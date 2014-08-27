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
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        common: 'js/common'
    }
});

require(['jquery', 'common'], function ($) {
    
    "use strict";
    
    $(document).ready(function () {
        (function () {
            var po = document.createElement('script');
            po.type = 'text/javascript';
            po.async = true;
            po.src = 'https://plus.google.com/js/client:plusone.js?onload=render';
            var s = document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(po, s);
        })();
      
        var signInCallback = function (result) {
            if (result['error']) {
                console.log('An error happened:', result['error']);
            } else {
                $('#code').attr('value', result['code']);
                $('#at').attr('value', result['access_token']);
                $('#google-plus').submit();
            }
        };
      
        function render() {
            gapi.signin.render('googleplus', {
                'scope': window.GOOGLE_DATA.scope,
                'clientid': window.GOOGLE_DATA.id,
                'accesstype': 'offline',
                'cookiepolicy': 'single_host_origin',
                'callback': 'signInCallback'
            });
        };
    });
    
    $(document).trigger('load');
    
});