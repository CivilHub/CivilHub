//
//
//

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
        ui: 'js/ui/ui',
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
        
        tagsinput: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'common',
         'js/locations/follow',
         'js/inviter/userinviter'],

function ($) {
    
    "use strict"
    
    $('.media-form-toggle').on('click', function (e) {
        e.preventDefault();
        $('#media-form').slideToggle('fast');
    });
});