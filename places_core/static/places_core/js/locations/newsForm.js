//
// locationForm.js
// ===============
//
define(['jquery',
        'underscore',
        'backbone',
        //'//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false',
        'js/editor/customCKEditor',
        'bootstrap-fileinput',
        'mapinput',
        'tagsinput'],

function ($, _, Backbone) {
    
    "use strict";
    
    var LocationForm = Backbone.View.extend({
        el:  "#news-create-form",
        
        initialize: function () {
            this.$el.find('#id_content').customCKEditor();
            //~ this.$el.find('[type="file"]').bootstrapFileInput();
            this.$el.find('#id_latitude').before('<div id="map"></div>');
            this.$el.find('#id_latitude, #id_longitude').css('display', 'none');
            //~ this.$el.find('#map').mapinput({
                //~ latField: '#id_latitude',
                //~ lngField: '#id_longitude',
                //~ width: 640,
                //~ height: 480
            //~ });
            this.$el.find('#id_tags').tagsInput({
                autocomplete_url: '/rest/tags/'
            });
        }
    });
    
    return LocationForm;
});