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
        paginator: 'includes/backbone/backbone.paginator',
        tagsinput: 'includes/jquery/jquery.tagsinput',
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
        },
        
        mapinput: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'js/ideas/votes/counterWindow',
         'js/common',
         'js/ideas/votes/votes',
         'js/comments/comments',
         'js/maps/pointer',
         'js/inviter/userinviter',
         'js/locations/follow',
         'js/ideas/category-creator'],

function ($, CounterWindow, Minimap) {
    
    "use strict";
    
    // Modal z podsumowanie głosów za i przeciw
    $('.idea-vote-count').on('click', function (e) {
        e.preventDefault();
        var ideaId = $(this).attr('data-target');
        var CW = CounterWindow.extend({
            'ideaId': ideaId
        });
        var cc = new CW();
    });
    
    $(document).trigger('load');
    
});