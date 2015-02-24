/*
 * vector-map.js
 * ==========
 * 
 * Skrypt odpowiadający za prawidłowe wyświetlanie vector-map
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        jpaginate: 'includes/jquery/jquery.paginate',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox',
        hammer: 'includes/mapplic/hammer',
        jeasing: 'includes/mapplic/jquery.easing',
        jmousewheel: 'includes/mapplic/jquery.mousewheel',
        mapplic: 'includes/mapplic/mapplic'
    },
    
    shim: {
        
        jpaginate: {
            deps: ['jquery']
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
        },
        
        tagsinput: {
            deps: ['jquery']
        },

        hammer: {
            deps: ['jquery']
        },

        jeasing: {
            deps: ['jquery']
        },

        jmousewheel: {
            deps: ['jquery']
        },

        mapplic: {
            deps: ['jquery']
        }
    }
});

require(['jquery',
         'js/modules/common',
         'hammer',
         'jeasing',
         'jmousewheel',
         'mapplic'],
         
function ($) {
    
    "use strict";
    
    $('#mapplic').mapplic({
        source: '/static/places_core/includes/mapplic/world.json',
        height: '100%',
        animate: true,
        sidebar: true,
        minimap: true,
        locations: true,
        deeplinking: true,
        fullscreen: false,
        hovertip: false,
        developer: false,
        maxscale: 4,
        zoom: true 
    });

    $(window).load(function() {

        $('.mapplic-sidebar').prepend('<div class="mapplicCountry"><p class="mappCountry">'gettext("Country")'</p><p>'gettext("Search by location")'<span class="fa fa-caret-down"></span></p></div>');

        $('.mapplicCountry').click(function(){
            $('.mapplic-search-form, .mapplic-list-container').toggle();
        });

        $('.mapplic-layer a').addClass('jump-marker');

    });

    $('.clear').hide();

    $(document).trigger('load');
    
});
