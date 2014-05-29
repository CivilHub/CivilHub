(function ($) {
    "use strict";
    //
    // jquery.mapinput
    //
    // This plugin provides more elegant way to handle latitude and longitude
    // inputs in forms with Google Map widget. I requires that google api
    // library is loaded as explained here:
    // https://developers.google.com/maps/documentation/javascript/tutorial#Loading_the_Maps_API
    // and that you have google API keys.
    // -------------------------------------------------------------------------
    //
    $.fn.mapinput = function (options) {
        $.fn.mapinput.defaults = {
            elementId: 'google-map-canvas', // Id of map element
            latField: '#latitude',          // Latitude field jquery selector
            lngField: '#longitude',         // Longitude -- "" --
            mapClass: 'mapinput-area',      // Classname for map element
            width:  300,                    // Map width in pixels
            height: 300,                    // Map height in pixels
            zoom:   8,                      // Initial zoom
            X:      -34.397,                // Initial position (lat)
            Y:      150.644,                // Initial position (lng)
            markerIcon: false               // Map marker icon (if provided)
        };
        options = $.fn.extend($.fn.mapinput.defaults, options);
        //
        // Core plugin function (jQuery plugin-like)
        // ---------------------------------------------------------------------
        //
        return $(this).each(function () {
            var $this = $(this),
                $map  = $('<div></div>'),
                $lat  = $this.find(options.latField),
                $lng  = $this.find(options.lngField),
                map   = null,
                marker= new google.maps.Marker(),
                mapOptions = {};
            // Hide existing form elements.
            $this.find('label, input').css('display', 'none')
            // Append element to draw map on.
            $map.appendTo($this).attr('id', options.elementId)
                .addClass(options.mapClass)
                .width(options.width).height(options.height);
            // Create google map with provided or default options.
            mapOptions = {
                center: new google.maps.LatLng(options.X, options.Y),
                zoom: options.zoom
            };
            map = new google.maps.Map(document.getElementById(options.elementId), 
                mapOptions);
            // Handle click event to place marker.
            google.maps.event.addListener(map, 'click', function(event) {
                var location = event.latLng;
                // Place marker on the map.
                marker.setMap(map);
                marker.setPosition(location);
                if (options.markerIcon) {
                    marker.setIcon(options.markerIcon);
                }
                // Set proper field values
                $lat.val(location.lat()).attr('value', location.lat());
                $lng.val(location.lng()).attr('value', location.lng());
            });
        });
    };
})(jQuery);