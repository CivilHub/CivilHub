//
// pointerModal.js
// ===============
//
define(['jquery',
        'underscore',
        'backbone',
        'mapinput'],

function ($, _, Backbone) {
    "use strict";
    
    var PointerModal = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'modal fade',
        
        initialize: function () {
            this.$el.html($('#map-marker-form-template').html());
            this.$el.modal({show:false});
            this.$el.find('#id_latitude').before('<div id="map"></div>');
            this.$el.find('#id_latitude, #id_longitude').css('display', 'none');
            this.$el.find('#map').mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 640,
                height: 480
            });
        },
        
        open: function () {
            this.$el.modal('show');
        },
        
        close: function () {
            this.$el.modal('hide');
        },
        
        submit: function () {
            
            formData = {
                content_type: $('#id_content_type').val(),
                object_pk   : $('#id_object_pk').val(),
                latitude    : $('#id_latitude').val(),
                longitude   : $('#id_longitude').val()
            }
            
            $.ajax({
                type: 'POST',
                
                url: this.$el.find('form:first').attr('action'),
                
                data: formData,
                
                success: function (resp) {
                    ui.message.success(resp.message);
                },
                
                error: function (err) {
                    console.log(err);
                }
            });
            
            $modal.modal('hide');
        }
    });
    
    return PointerModal;
});