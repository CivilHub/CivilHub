//
// pointer.js
// ==========
//
// Script to load when you want to use map pointer form.

require(['jquery',
         'js/modules/utils/utils',
         'js/modules/ui/ui',
         'js/modules/ui/mapinput'],

function ($, utils, ui) {

  "use strict";

  $('.map-marker-toggle').bind('click', function (evt) {

    evt.preventDefault();

    var $modal   = $(_.template($('#map-marker-form-template').html(), {})),
        $form    = $modal.find('form:first'),
        $submit  = $modal.find('.submit-btn:first'),
        formData = {};

    $modal.modal('show');

    $modal.on('shown.bs.modal', function () {

      $('#id_latitude').before('<div class="mapinput"></div>');

      $modal.find('.submit-btn').on('click', function (e) {
        e.preventDefault();
        $form.submit();
      });

      var markersUrl = ('/api-maps/objects/?ct={ct}&pk={pk}')
        .replace(/{ct}/g, $('#id_content_type').val())
        .replace(/{pk}/g, $('#id_object_pk').val());

      $.get(markersUrl, function (markers) {
        $('.mapinput').mapinput({
          single: false,
          width: 550,
          height: 300,
          markers: markers,
          iconPath: ([window.STATIC_URL, 'css', 'images']).join('/')
        });
      });

      $form.on('submit', function (e) {
        e.preventDefault();
        formData = {
          csrfmiddlewaretoken: utils.getCookie('csrftoken'),
          content_type: $('#id_content_type').val(),
          object_pk: $('#id_object_pk').val(),
          location: $('#current-location-pk').val(),
          markers: JSON.stringify($.map($('.mapinput').data('mapinput').markers,
            function (m) {
              return {lat: m.getLatLng().lat, lng: m.getLatLng().lng};
            }
          ))
        };
        console.log(formData);
        $.post('/api-maps/mapinput/', formData,
          function (response) {
            ui.message.success(gettext("Map pointer created"));
          }
        );

        $modal.modal('hide');
      });
    });

    $modal.on('hidden.bs.modal', function () {
      $modal.empty().remove();
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    });
  });
});