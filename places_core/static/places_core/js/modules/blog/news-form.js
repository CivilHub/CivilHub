//
// news-form.js
// ============

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'redactor',
         'tagsinput',
         'js/modules/ui/mapinput'],

function ($, _, utils) {

  "use strict";

  $(document).ready(function () {

    var map = null;

    $('#id_content').redactor({
      buttons: ['bold', 'italic', 'unorderedlist', 'orderedlist', 'link'],
      plugins: ['uploader']
    });

    $('#id_tags').tagsInput({
      autocomplete_url: '/rest/tags/',
      defaultText: gettext("Add tag")
    });

    function createMap (markers) {
      map = $('.mapinput').mapinput({
        single: false,
        width: 550,
        height: 300,
        markers: markers || [],
        iconPath: ([window.STATIC_URL, 'css', 'images']).join('/')
      }).data('mapinput');
    }

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
      var url = ('/api-maps/objects/?ct={ct}&pk={pk}')
        .replace(/{ct}/g, civapp.ct)
        .replace(/{pk}/g, civapp.pk);

      $.get(url, function (markers) {
        createMap(markers);
        $('#news-create-form').on('submit', function (e) {
          submitMarkers(civapp.ct, civapp.pk)
        });
      });
    } else {
      createMap();
    }
  });

});
