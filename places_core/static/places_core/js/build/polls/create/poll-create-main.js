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
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone'
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
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        tagsinput: {
            deps: ['jqueryui']
        }
    }
});

require(['jquery',
         'js/common',
         'js/locations/follow',
         'js/inviter/userinviter',
         'js/polls/poll-form/create-poll'],

function ($, _) {
    
    "use strict";
    
    $(document).trigger('load');
    
});