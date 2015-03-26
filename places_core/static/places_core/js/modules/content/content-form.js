//
// content-form.js
// ===============
//

// We add those scripts to forms that have a map.
// The condition for the script to work is that the form
// must have the ID 'content-create-form'.

require(['jquery',
         'js/modules/utils/utils',
         'js/modules/ui/mapinput'],

function ($, utils) {

  "use strict";

  $(document).ready(function () {

    // NOTE: UWAGA: I presume that in the form there is only ONE map!
    var map = null;

    // Edition of non-existing object, we send markers separately
    //
    // @param { Number } content type ID
    // @param { Number } object ID

    function submitMarkers (ct, pk) {
      var url = '/api-maps/mapinput/';
      var data = {
          csrfmiddlewaretoken: utils.getCookie('csrftoken'),
          content_type: civapp.ct,
          object_pk: civapp.pk,
          markers: JSON.stringify(_.map(map.markers, function (m) {
            return {lat: m.getLatLng().lat, lng: m.getLatLng().lng};
          }))
        };

      $.post(url, data, function (response) {
        console.log(response);
      });
    }

    if (window.civapp !== undefined) {

      // We edit an non-existing object

      var url = ('/api-maps/objects/?ct={ct}&pk={pk}')
        .replace(/{ct}/g, civapp.ct)
        .replace(/{pk}/g, civapp.pk);

      $.get(url, function (markers) {
        map = $('.mapinput').mapinput({
          single: false,
          width: 550,
          height: 300,
          markers: markers || [],
          iconPath: ([window.STATIC_URL, 'css', 'images']).join('/'),
          tileUrl: 'https://b.tiles.mapbox.com/v4/grzegorz21.k01pjfol/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3J6ZWdvcnoyMSIsImEiOiJPX0F1MWJvIn0.sciNGCKR54oCVhfSYPFCCw'
        }).data('mapinput');
        $('#content-create-form').on('submit', function (e) {
          submitMarkers(civapp.ct, civapp.pk);
        });
      });

    } else {

      // We add a new object - in this case we send an additional
      // field in the form and in it (JSON-ENCODED(!!!)) markers. 

      var $i = $('<input type="hidden" name="markers" />');

      $('#content-create-form').append($i);

      map = $('.mapinput').mapinput({
        single: false,
        width: 550,
        height: 300,
        iconPath: ([window.STATIC_URL, 'css', 'images']).join('/'),
        onchange: function (e, markers) {
          $i.val(JSON.stringify(_.map(markers, function (m) {
            return {'lat': m.getLatLng().lat, 'lng': m.getLatLng().lng};
          })));
        }
      }).data('mapinput');
    }
  });

});