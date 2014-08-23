//
// Lista wpisów na blogu
//  => /templates/locations/location_news.html
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
        bootbox: 'includes/bootstrap/bootbox',
        ui: 'js/ui/ui',
        list: 'js/topics/news-list/niew',
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
         'js/blog/news-list/blog',
         'ui',
         'common',
         'js/locations/follow',
         'js/blog/category-creator',
         'js/inviter/userinviter'], 
         
function ($) {

    "use strict";

    $(document).trigger('load');
    
});