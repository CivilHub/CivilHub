//
// Lista idei
//  => /templates/locations/location_ideas.html
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
        paginator: 'includes/backbone/backbone.paginator',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
        common: 'js/common',
        moment: 'includes/momentjs/moment'
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
        
        tagsinput: {
            deps: ['jquery']
        },
    }
});

require(['jquery',
         'utils',
         'ui',
         'common',
         'js/locations/follow',
         'js/ideas/idea-list/ideas',
         'js/ideas/votes/votes',
         'js/ideas/category-creator',
         'js/inviter/userinviter'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
    
});