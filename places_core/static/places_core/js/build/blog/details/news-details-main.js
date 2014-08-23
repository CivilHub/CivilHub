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
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        paginator: 'includes/backbone/backbone.paginator',
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
         'ui',
         'common',
         'js/locations/follow',
         'js/maps/minimap',
         'js/maps/pointer',
         'js/comments/comments',
         'js/blog/category-creator',
         'js/inviter/userinviter'], 
         
function ($) {
    
    "use strict";
    
    setTimeout(function () {
        if (window.MARKERS.length > 0) {
            $('#minimap').minimap(minimapData);
        }
    }, 2000);
    
    $(document).trigger('load');
    
});