//
// jquery.mapinput.js
// ==================
//
// Mapinput AMD module.

require(['jquery', 'leaflet'],
        
function ($, L) {
    
    "use strict";

    // jquery.mapinput
    // ---------------

    $.fn.mapinput = function (options) {
        
        var defaults = {
            center: [0, 0],
            zoom: 2,
            maxZoom: 18,
            width: 300,
            height: 300,
            elementID: 'map-canvas',
            latField: '#latitude',
            lngField: '#longitude',
            attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
        };
        
        return $(this).each(function () {
            var $el = $(this),
                $map = $('<div></div>'),
                map = null,
                marker = null,
                opts = $.extend(defaults, options);

            $el.find('label', 'input').css('display', 'none');
            
            $map.appendTo($el).attr('id', opts.elementID)
                .css('width', opts.width).css('height', opts.height);
            
            map = L.map(opts.elementID).setView(opts.center, opts.zoom);
            
            L.tileLayer('https://b.tiles.mapbox.com/v4/grzegorz21.k01pjfol/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3J6ZWdvcnoyMSIsImEiOiJPX0F1MWJvIn0.sciNGCKR54oCVhfSYPFCCw', {
                attribution: opts.attribution,
                maxZoom: opts.maxZoom
            }).addTo(map);
            
            L.Icon.Default.imagePath = 
                    ([window.STATIC_URL, 'css', 'images']).join('/');
            
            map.on('click', function (e) {
                if (marker !== null) map.removeLayer(marker);
                marker = L.marker([e.latlng.lat, e.latlng.lng]).addTo(map);
                $(opts.latField).val(e.latlng.lat);
                $(opts.lngField).val(e.latlng.lng);
            });
        });
    };
});