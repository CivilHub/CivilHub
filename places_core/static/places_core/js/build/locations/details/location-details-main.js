//
//
//

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        fileinput: 'includes/bootstrap/bootstrap.file-input'
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
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        fileinput: {
            deps: ['bootstrap']
        },
        
        tagsinput: {
            deps: ['jquery']
        },
    }
});

require(['jquery',
         'js/locations/actions/actions',
         'js/common',
         'js/locations/follow',
         'js/inviter/userinviter',
         'js/locations/background'],

function($) {
    
    "use strict";

    $(document).trigger('load');
    
});
