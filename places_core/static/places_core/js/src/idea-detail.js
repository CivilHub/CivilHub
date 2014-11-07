/*
 * idea-detail.js
 * ==============
 * 
 * Szczegółowy widok pojedynczej idei.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone",
        paginator  : "includes/backbone/backbone.paginator",
        tagsinput  : "includes/jquery/jquery.tagsinput",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        moment     : "includes/momentjs/moment",
        leaflet    : "includes/leaflet/leaflet"
    },
    
    shim: {
        
        jpaginate: {
            deps: ["jquery"]
        },
        
        underscore: {
            deps: ["jquery"],
            exports: "_"
        },
        
        backbone: {
            deps: ["underscore"],
            exports: "Backbone"
        },
        
        bootstrap: {
            deps: ["jquery"]
        },
        
        bootbox: {
            deps: ["bootstrap"],
            exports: "bootbox"
        },
        
        tagsinput: {
            deps: ["jquery"]
        },
        
        mapinput: {
            deps: ["jquery"]
        }
    }
});

require(['jquery',
         'js/modules/ideas/votes/counterWindow',
         'js/modules/common',
         'js/modules/ideas/votes/votes',
         'js/modules/comments/comments',
         'js/modules/maps/pointer',
         'js/modules/inviter/userinviter',
         'js/modules/locations/follow',
         'js/modules/ideas/category-creator'],

function ($, CounterWindow) {
    
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