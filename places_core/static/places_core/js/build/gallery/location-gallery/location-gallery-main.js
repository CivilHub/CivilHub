//
// user-gallery-main.js
// ====================
//
// Skrypty dla głównego widoku galerii miejsca.
//  => /templates/gallery/location-gallery.html

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
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
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        }
    }
});

require(['jquery',
         'js/ui/ui',
         'js/locations/follow',
         'js/common'],

function ($, ui) {
    
    "use strict";
    
    $('.control-delete').on('click', function (e) {
        e.preventDefault();
        var href = $(this).attr('href');
        ui.confirmWindow(function () {
            document.location.href = href;
        });
    });
    
    $(document).trigger('load');
});