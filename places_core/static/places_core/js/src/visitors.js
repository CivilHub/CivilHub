//
// visitors.js
// ===========

// Shows map with currently active visitors that we are able to track.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'underscore',
           'js/modules/common',
           'js/modules/ui/mapinput'],

  function ($, _) {
    "use strict";
    $(document).ready(function () {
      var $el = $('#map');
      var markers = JSON.parse($el.attr('data-markers'));

      // Remove empty markers
      markers = _.reject(markers, function (m) {
        return _.isEmpty(m);
      });

      // Convert geodata to format understandable by Leaflet
      markers = _.map(markers, function (m) {
        return { lat: m.latitude, lng: m.longitude };
      });

      $el.mapinput({ markers: markers });
    });
  });
});
