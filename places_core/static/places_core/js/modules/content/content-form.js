//
// content-form.js
// ===============
//

// Add this scripts to forms with map inside. Form must have id 'content-form'.

require(['jquery',
         'js/modules/utils/utils',
         'js/modules/ui/mapinput'],

function ($, utils) {

"use strict";

$(document).ready(function () {

  // WARNING: I suppose that there is only one map!
  var map = null;

  // Edit existing object - send markers via Ajax
  //
  // @param { Number } Content Type ID
  // @param { Number } Object ID

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

    // Edit existing object

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

    // Create new object

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