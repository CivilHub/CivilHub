//
// Widok pojedynczego wpisu na blogu
//  => /templates/blog/news_detail.html
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        paginator: 'includes/backbone/backbone.paginator',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
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
        }
    }
});

require(['jquery',
         'js/maps/minimap',
         'js/common',
         'js/locations/follow',
         'js/maps/pointer',
         'js/comments/comments',
         'js/blog/category-creator',
         'js/inviter/userinviter'], 
         
function ($, Minimap) {
    
    "use strict";
    
    // Minimapa z markerami (jeżeli są jakieś)
    $(document).ready(function () {
        var minimap = new Minimap(window.MARKERS);
        $('.minimap-toggle-button').on('click', function (e) {
            e.preventDefault();
            minimap.open();
        });
    });
    
    $(document).trigger('load');
    
});