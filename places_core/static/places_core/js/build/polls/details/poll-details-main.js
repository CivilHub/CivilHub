//
// Strona ankiety => /templates/polls/poll-details.html
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    //urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common',
        async: 'includes/require/async',
        moment: 'includes/momentjs/moment',
        mapinput: 'js/ui/jquery.mapinput',
        bootbox: 'includes/bootstrap/bootbox'
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
         'js/maps/minimap',
         'js/maps/pointer',
         'js/locations/follow',
         'js/inviter/userinviter'],

function ($) {
    
    "use strict";
    
    var runMinimap = function () {
        
        if (pollapp.markers.length > 0) {
            $('#minimap').minimap(pollapp.markers);
        }
        
        return false;
    };
    
    setTimeout(function () {
        runMinimap();
    }, 2000);
    
    $(document).trigger('load');
    
});