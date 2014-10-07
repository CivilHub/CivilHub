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
        jqueryui: { deps: ['jquery'] },
        
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
    
    // Create main map application
    
    var app = new CivilMap({
        elementID: 'main-map',
        center: [window.CIVILAPP.position.lat, window.CIVILAPP.position.lng]
    });
    
    // Get map content filters
    
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
    
    // Simplified autocomplete functionality to search for places - it allows
    // users to find and select single location to browse markers from.
    
    $.fn.autocomplete = function () {
        var $ul = $('<ul class="custom-autocomplete"></ul>'),
            tpl = '<li><a href="#" data-location="{id}" data-lat="{lat}" \
                  data-lng="{lng}">{name}</a></li>';
        
        function clearItems () {
            $ul.find('li').empty().remove();
        }
            
        return $(this).each(function () {
            
            var $input = $(this);
            $ul.insertAfter($input);
            
            $input.on('keyup', function () {
                
                if ($input.val().length === 0) {
                    app.setLocation(null);
                    app.fetchData();
                    return false;
                }
                
                $.get('/api-locations/markers/', {term: $input.val()},
                    function (response) {
                        clearItems();
                        $.each(response.results, function (idx, item) {
                            var $li = $(tpl.replace(/{id}/g, item.id)
                                           .replace(/{name}/g, item.name)
                                           .replace(/{lat}/g, item.latitude)
                                           .replace(/{lng}/g, item.longitude));
                            $li.appendTo($ul);
                            $li.find('a').on('click', function (e) {
                                e.preventDefault();
                                $input.val($(this).text());
                                app.setLocation($(this).data());
                                clearItems();
                            });
                        });
                    }
                );
            });
            
            $input.on('click', function () {
                if ($ul.find('li').length >= 1) {
                    $ul.toggle();
                }
            });
        });
    };
    
    $('.map-filter-toggle').change(function () {
        app.setFilters(getFilters());
    });
    
    $('.angle-icon-toggle').on('click', function () {
        $('#map-options-panel').slideToggle('fast');
    });
    
    $('#select-location-field').autocomplete();
    
    $(document).trigger('load');
    
});