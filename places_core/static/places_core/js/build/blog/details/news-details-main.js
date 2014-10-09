//
// Widok pojedynczego wpisu na blogu
//  => /templates/blog/news_detail.html
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        paginator: 'includes/backbone/backbone.paginator',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        moment: 'includes/momentjs/moment',
        leaflet: 'includes/leaflet/leaflet'
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
        }
    }
});

require(['jquery',
         'js/common',
         'js/locations/follow',
         'js/maps/pointer',
         'js/comments/comments',
         'js/blog/category-creator',
         'js/inviter/userinviter'], 
         
function ($, Minimap) {
    
    "use strict";
    
    $(document).trigger('load');
    
});