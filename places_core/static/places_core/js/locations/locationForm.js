//
// locationForm.js
// ===============
//
define(['jquery',
        'underscore',
        'backbone',
        'mapinput',
        'async!//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false',
        'js/editor/customCKEditor',
        'bootstrap-fileinput'],

function ($, _, Backbone) {
    
    "use strict";
    
    var LocationForm = Backbone.View.extend({
        el:  "#new-location-form",
        
        initialize: function () {
            this.$el.find('#id_description').customCKEditor('custom');
            this.$el.find('[type="file"]').bootstrapFileInput();
            this.$el.find('#id_latitude').before('<div id="map"></div>');
            this.$el.find('#id_latitude, #id_longitude').css('display', 'none');
            this.$el.find('#map').mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 640,
                height: 480
            });
        }
    });
    
    return LocationForm;
});