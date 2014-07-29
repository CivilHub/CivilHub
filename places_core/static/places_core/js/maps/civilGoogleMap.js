//
// civilGoogleMap.js
// =================
// Main map to show everything :)
define(['jquery',
        'bootstrap',
        '//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false&callback=initializeMainMap',
        'js/maps/markerclusterer'],

function ($) {
    "use strict";
    
    //
    // Fetch objects from server and create map.
    // -----------------------------------------------------------------------------
    //
    var fetchMap = function (url) {
        $.get(url, function (resp) {
            var markers = [], map = null;
            resp = JSON.parse(resp);
            if (resp.success) {
                $(resp.locations).each(function () {
                    markers.push(this);
                });
                $(resp.pointers).each(function () {
                    markers.push(this);
                });
                map = civilGoogleMap(markers);
                $('.map-filter-toggle').bind('change', function (evt) {
                    evt.preventDefault;
                    map.refreshMap(getFilters());
                });
            } else {
                console.log(gettext("Failed to load map data"));
            }
        });
    };
    
    window.initializeMainMap = function () {
        fetchMap('/maps/pointers/');
    };
    
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
                            icon: '/static/maps/icons/marker-' + mapData[i].content_object.type + '.png'
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
                        url: '/static/maps/images/people35.png',
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
    
    //
    // Only followed locations button.
    // -----------------------------------------------------------------------------
    //
    $('#map-follow-toggle').on('click', function (e) {
        var $icon = $(this).find('.fa:first');
        e.preventDefault();
        $('#map').empty();
        if ($icon.hasClass('fa-circle-o')) {
            fetchMap('/maps/pointers/?followed=true');
        } else {
            fetchMap('/maps/pointers/');
        }
        $icon.toggleClass('fa-circle-o').toggleClass('fa-check-circle-o');
    }).tooltip({placement:'right'});
    
    return fetchMap;
});