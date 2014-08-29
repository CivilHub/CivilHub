//
// Konfiguracja dla google mapy.
// -----------------------------------------------------------------------------

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone'
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

define('gmaps', ['async!//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false'], function () {
    return google.maps;
});

require(['jquery',
         'gmaps',
         'js/maps/map',
         'js/common'],

function ($, CivilMap) {
    
    "use strict";
    
    (function () {
        var topAdjust = $('#navbar-top').height(),
            $map      = $('#map'),
            $toggle   = $('#map-filter-toggle'),
            $panel    = $('#map-options-panel');

        $map.css({
            position : "absolute",
            left     : 0,
            top      : topAdjust,
            width    : "100%",
            height   : $(window).height() - topAdjust,
            'z-index': 10
        });

        $toggle // show/hide map options button.
            .tooltip({placement:'right'})
            .bind('click', function (evt) {
                evt.preventDefault();
                $panel.slideToggle('fast');
                $toggle.find('.fa')
                    .toggleClass('fa-arrow-circle-down')
                    .toggleClass('fa-arrow-circle-up');
            });
    })();
    
    window.getFilterTypes = function () {
        var $filters = $('#map-options-panel').find('[type="checkbox"]');
        var contentTypes = [];
        $filters.each(function () {
            if ($(this).is(':checked')) {
                contentTypes.push(_.findWhere(CONTENT_TYPES, 
                    {model:$(this).attr('data-target')}).content_type);
            }
        });
        return contentTypes;
    };
    
    window.mapDialogTpl = _.template($('#map-dialog-tpl').html());
    window.locDialogTpl = _.template($('#loc-dialog-tpl').html());
    
    window.app = {};
    
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: window.MAP_DATA.zoom,
        center: new google.maps.LatLng(
            window.MAP_DATA.lat,
            window.MAP_DATA.lng
        )
    });
    
    $.get(window.MAP_DATA.url, function (resp) {
        window.app = new CivilMap(map, resp);
    });
    
    $('#map-options-panel').find('[type="checkbox"]').on('change',
        function () {
            window.app.filter(getFilterTypes());
        }
    );
    
    $('#country-nav-form-country').on('change', function () {
        app.changeCountry($(this).val());
    });
    
    $(document).trigger('load');
    
});