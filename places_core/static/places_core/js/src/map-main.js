//
// map-main.js
// ===========
// 
// Główna mapa.

require([window.STATIC_URL + "/js/config.js"], function () {
    require(['jquery',
             'js/modules/maps/map',
             'js/modules/maps/autocomplete',
             'bootstrap',
             'js/modules/common/bookmarks',
             'tour',
             'js/modules/bouncy-navigation/main'],

    function ($, CivilMap) {
        
        "use strict";
        
        // Set to true when map is activated to avoid
        // initializing map second time.
        var mapIsActive = false;
        
        function getCoords (success) {
            
            var callback = null;
            
            if (success !== undefined && typeof(success) === 'function') {
                callback = success;
            } else {
                callback = function (x, y) {console.log(x,y);};
            }
            
            var fallback = function () {
                var x = window.CIVILAPP.position.lat;
                var y = window.CIVILAPP.position.lng;
                callback(x, y);
            };
            
            if (navigator.geolocation !== null && "geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    var x = position.coords.latitude;
                    var y = position.coords.longitude;
                    callback(x, y);
                    // If user selected 'later' or 'not this time' when asked for
                    // his/her position.
                    setTimeout(function () {
                        if (!mapIsActive) {
                            fallback();
                        }
                    }, 5000);
                }, function () {
                    fallback();
                });
            } else {
                fallback();
            }
        }
        
        getCoords(function (lat, lng) {
            
            var app = {
            
                // Create main map application
                
                application: new CivilMap({
                    elementID: 'main-map',
                    center: [lat, lng],
                    mapTailURL: 'https://b.tiles.mapbox.com/v4/grzegorz21.k01pjfol/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3J6ZWdvcnoyMSIsImEiOiJPX0F1MWJvIn0.sciNGCKR54oCVhfSYPFCCw'
                }),
                
                // Get map content filters
                
                getFilters: function getFilters () {
                    var filters = [], t = '', ct = null;
                    $('.map-filter-toggle').each(function () {
                        if ($(this).is(':checked')) {
                            t = $(this).attr('data-target');
                            ct = _.findWhere(window.CONTENT_TYPES, {model: t});
                            filters.push(ct.content_type);
                        }
                    });
                    return filters;
                },
                
                // Initialize all plugins
                
                initialize: function () {
                    $('.map-filter-toggle').change(function () {
                        this.application.setFilters(this.getFilters());
                    }.bind(this));
                    
                    $('.angle-icon-toggle').on('click', function () {
                        $('#map-options-panel').slideToggle('fast');
                    });
                    
                    $('#select-location-field').autocomplete({
                        onSelect: function (locationID) {
                            app.application.setLocation(locationID);
                        },
                        onClear: function () {
                            app.application.setLocation(null);
                            app.application.fetchData();
                        }
                    });
                    
                    mapIsActive = true;
                }
            };
            
            if (!mapIsActive) {
                app.initialize();
            }
        });
        $('.custom-tooltip-right').tooltip({placement : 'right'});
        $('.navbar-avatar').tooltip({ placement : 'bottom'});

        $(document).trigger('load');
        
    });
});