//
// map.js
// ======
// Entry point for Google Maps.
//
require(['jquery',
         'bootstrap',
         'js/maps/markerclusterer',
         '//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false&callback=initializeMainMap',],

function ($) {
    
    "use strict";
    
    var running = false;
    
    function civilGoogleMap(mapData) {
        
        var imageUrl = 'http://chart.apis.google.com/chart?cht=mm&chs=24x32&' +
            'chco=FFFFFF,008CFF,000000&ext=.png';
            
        var dialogTemplate = _.template($('#map-dialog-tpl').html());
        
        var map = {
            map: null,
            markerClusterer: null,
                
            refreshMap: function (filters) {
                var _this = this,
                    markers = [],
                    i,
                    markerImage = new google.maps.MarkerImage(imageUrl,
                        new google.maps.Size(24, 32));
                        
                if (_this.markerClusterer) {
                    _this.markerClusterer.clearMarkers();
                }
                
                for (i = 0; i < mapData.length; ++i) {
                    var latLng = new google.maps.LatLng(mapData[i].lat,
                            mapData[i].lng),
                        marker = new google.maps.Marker({
                            position: latLng,
                            icon: window.STATIC_URL + '/icons/marker-' + mapData[i].content_object.type + '.png'
                        });
                    $.extend(marker, mapData[i]);
                    if (filters && filters.indexOf(marker.content_object.type) >= 0 || !filters) {
                        
                        (function (m) {
                            
                            markers.push(m);
                            
                            google.maps.event.addListener(m, 'click', function () {
                                var contentString = dialogTemplate({
                                    url: m.content_object.url,
                                    type: m.content_object.type,
                                    title: m.content_object.title,
                                    desc: m.content_object.desc,
                                    date: m.content_object.date,
                                    img: m.content_object.img,
                                    user: m.content_object.user,
                                    profile: m.content_object.profile
                                });
                                
                                var infoWindow = new google.maps.InfoWindow({
                                    content: contentString
                                });
                                
                                infoWindow.open(_this.map, m);
                            });
                            
                        })(marker);
                    }
                }
                
                _this.markerClusterer = new MarkerClusterer(_this.map, markers, {
                    maxZoom: 10,
                    gridSize: 30,
                    styles: [{
                        url: window.STATIC_URL + '/images/people35.png',
                        height: 35,
                        width: 35,
                        anchor: [16, 0],
                        textColor: '#ff00ff',
                        textSize: 10
                    }]
                });
            },
            
            initialize: function () {
                var _this = this,
                    refresh = document.getElementById('refresh'),
                    clear = document.getElementById('clear');
                    
                _this.map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 4,
                    center: new google.maps.LatLng(52.0, 23.0)
                });
                
                _this.refreshMap();
            },
            
            clearClusters: function (e) {
                e.preventDefault();
                e.stopPropagation();
                this.markerClusterer.clearMarkers();
            }
        };
        
        map.initialize();
        
        return map;
    };
    
    //
    // Fetch objects from server and create map.
    // -----------------------------------------------------------------------------
    //
    var fetchMap = function (url) {
        running = true;
        $.get(url, function (resp) {
            var markers = [];
            resp = JSON.parse(resp);
            if (resp.success) {
                $(resp.locations).each(function () {
                    markers.push(this);
                });
                $(resp.pointers).each(function () {
                    markers.push(this);
                });
                window.CivilMap = civilGoogleMap(markers);
                $('.map-filter-toggle').bind('change', function (evt) {
                    evt.preventDefault;
                    window.CivilMap.refreshMap(getFilters());
                });
            } else {
                console.log(gettext("Failed to load map data"));
            }
        });
    };
    
    window.initializeMainMap = function () {
        fetchMap('/maps/pointers/');
    };
    
    setTimeout(function () {
        if (_.isUndefined(window.CivilMap) && !mapRunning) {
            initializeMainMap();
        }
    }, 3000);
    
    //
    // Adjust map size to device screen and bind events to show/hide menu button.
    // -------------------------------------------------------------------------
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