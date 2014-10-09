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
        }
        
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
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: opts.attribution,
                maxZoom: opts.maxZoom
            }).addTo(map);
            
            map.on('click', function (e) {
                if (marker !== null) map.removeLayer(marker);
                marker = L.marker([e.latlng.lat, e.latlng.lng]).addTo(map);
                $(opts.latField).val(e.latlng.lat);
                $(opts.lngField).val(e.latlng.lng);
            });
        });
    };
});