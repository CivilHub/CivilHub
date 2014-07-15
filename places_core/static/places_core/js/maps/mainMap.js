//
// Google Maps API.
// ================
//
require(['jquery',
         'bootstrap',
         '/static/places_core/js/maps/civilGoogleMap.js',
         '//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false&callback=initializeMainMap'],

function ($) {
    
    "use strict";
    //
    // Adjust map size to device screen and bind events to show/hide menu button.
    // -----------------------------------------------------------------------------
    //
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

        //$panel.hide();

        $toggle // show/hide map options button.
            .tooltip({placement:'right'})
            .bind('click',
                function (evt) {
                    evt.preventDefault();
                    $panel.slideToggle('fast');
                    $toggle.find('.fa')
                        .toggleClass('fa-arrow-circle-down')
                        .toggleClass('fa-arrow-circle-up');
                }
            );

    })();

    // Shortcut to get list of active filters
    var getFilters = function () {
        var filterToggles = $('.map-filter-toggle'),
            filters = [];
            
        filterToggles.each(function () {
            if ($(this).is(':checked')) {
                filters.push($(this).attr('data-target'));
            }
        });
        
        return filters;
    };
});
