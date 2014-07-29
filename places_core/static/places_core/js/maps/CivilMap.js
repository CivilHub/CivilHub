//
// CivilMap.js
// ===========
// Returns proper Google Maps object
//
define(['jquery',
        'underscore',
        'js/maps/markerclusterer',
        '//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false'],


function ($, _) {
    "use strict";
    
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
    
    return civilGoogleMap;
});