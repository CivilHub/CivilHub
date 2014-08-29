//
// Forma do tworzenia nowej dyskusji
//
//  => /templates/locations/location_forum_create.html
//
// -----------------------------------------------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 300,
    
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        'bootstrap-switch': 'includes/bootstrap/bootstrap-switch',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone'
    },
    
    shim: {
        
        jqueryui: {
            deps: ['jquery']
        },
        
        tagsinput: {
            deps: ['jqueryui']
        },
        
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
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        'bootstrap-switch': {
            deps: ['bootstrap']
        },
        
        mapinput: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'js/common',
         'js/locations/follow',
         'js/inviter/userinviter',
         'js/topics/discussion-form',
         'js/topics/category-creator'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
    
});
