/*
 * blog-details.js
 * ===============
 * 
 * Detailed view of single aticles blog page.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        jpaginate: 'includes/jquery/jquery.paginate',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        paginator: 'includes/backbone/backbone.paginator',
        moment: 'includes/momentjs/moment'
    },
    
    shim: {
        
        jpaginate: {
            deps: ['jquery'],
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
        }
    }
});

require(['jquery',
         'js/modules/common',
         'js/modules/comments/comments'],

function ($) {
    
    "use strict";
    
    $(document).trigger('load');
    
});