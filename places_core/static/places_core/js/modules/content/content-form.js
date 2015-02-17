//
// content-form.js
// ===============
//

// Dodajemy te skrypty do formularzy w których jest mapa.
// Warunek działania skryptu jest taki, że formularz musi
// mieć ID 'content-create-form'.

require(['jquery',
         'js/modules/utils/utils',
         'js/modules/ui/mapinput'],

function ($, utils) {

  "use strict";

  $(document).ready(function () {

    // UWAGA: zakładam, że w formularzu jest JEDNA mapa!
    var map = null;

    // Edytując istniejący obiekt, wysyłamy markery osobno
    //
    // @param { Number } ID typu zawartości
    // @param { Number } ID obiektu

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

      // Edytujemy istniejący obiekt

      var url = ('/api-maps/objects/?ct={ct}&pk={pk}')
        .replace(/{ct}/g, civapp.ct)
        .replace(/{pk}/g, civapp.pk);

      $.get(url, function (markers) {
        map = $('.mapinput').mapinput({
          single: false,
          width: 550,
          height: 300,
          markers: markers || [],
          iconPath: ([window.STATIC_URL, 'css', 'images']).join('/')
        }).data('mapinput');
        $('#content-create-form').on('submit', function (e) {
          submitMarkers(civapp.ct, civapp.pk);
        });
      });

    } else {

      // Dodajemy nowy obiekt - w tym przypadku przesyłamy dodatkowe
      // pole w formularzu, a w nim (JSON-ENCODED(!!!)) markery.

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