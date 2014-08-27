//
// Szczegółowy widok artykułu
//
//  => /templates/articles/article.html
//
// --------------------------------------------------

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
        moment: 'includes/momentjs/moment',
        ui: 'js/ui/ui',
        utils: 'js/utils/utils',
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
        }
    }
});

require(['jquery',
         'common',
         'js/comments/comments'],

function ($) {
    
    $(document).trigger('load');
    
});