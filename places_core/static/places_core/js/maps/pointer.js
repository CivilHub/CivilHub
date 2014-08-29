//
// pointer.js
// ==========
//
// Script to load when you want to use map pointer form.

require(['jquery',
         'js/utils/utils',
         'js/ui/ui',
         'js/ui/mapinput'],

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
            
            $('#id_latitude').before('<div id="map"></div>');
            $('#map').mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 550,
                height: 300
            });
            
            $form.on('submit', function (evt) {
                evt.preventDefault();
            });
            
            $submit.on('click', function () {
                formData = {
                    content_type: $('#id_content_type').val(),
                    object_pk   : $('#id_object_pk').val(),
                    latitude    : $('#id_latitude').val(),
                    longitude   : $('#id_longitude').val()
                }
                
                $.ajax({
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", utils.getCookie('csrftoken'));
                    },
                    type: 'POST',
                    url: $form.attr('action'),
                    data: formData,
                    dataType: 'json',
                    success: function (resp) {
                        ui.message.success(resp.message);
                    },
                    error: function (err) {
                        console.log(err);
                    }
                });
                
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