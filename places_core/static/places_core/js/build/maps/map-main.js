//
// Konfiguracja dla google mapy.
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
        bootbox: 'includes/bootstrap/bootbox',
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
         'js/maps/map',
         'bootstrap',
         'js/common/bookmarks'],

function ($, CivilMap) {
    
    "use strict";
    
    var app = new CivilMap({
        elementID: 'main-map',
        center: [window.CIVILAPP.position.lat, window.CIVILAPP.position.lng]
    });
    
    function getFilters () {
        var filters = [], t = '', ct = null;
        $('.map-filter-toggle').each(function () {
            if ($(this).is(':checked')) {
                t = $(this).attr('data-target');
                ct = _.findWhere(window.CONTENT_TYPES, {model: t});
                filters.push(ct.content_type);
            }
        });
        return filters;
    }
    
    $('.map-filter-toggle').change(function () {
        app.setFilters(getFilters());
    });
    
    $('.angle-icon-toggle').on('click', function () {
        $('#map-options-panel').slideToggle('fast');
    });
    
    $(document).trigger('load');
    
});