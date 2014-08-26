//
// Strona wyświetlania wyników ankiety 
//
//  => /templates/polls/poll-results.html
//
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common',
    },
    
    shim: {
        underscore: {
            deps: ['jquery'],
            exports: '_'
        },
        
        jqueryui: {
            deps: ['jquery']
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
         'underscore',
         'bootstrap',
         'common',
         'js/locations/follow',
         'js/inviter/userinviter',
         'js/polls/poll-form/create-poll'],

function ($, _) {
    
    "use strict";
    
    $(document).trigger('load');
    
});