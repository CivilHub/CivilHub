//
// discussionForm.js
// =================
//
define(['jquery',
        'underscore',
        'backbone',
        'async!//maps.googleapis.com/maps/api/js?keyAIzaSyD9xJ_hO0PSwdf-8jaTKMAJRcy9USx7YjA&sensor=false',
        'js/editor/customCKEditor',
        'bootstrap-switch',
        'tagsinput',
        'mapinput'],

function ($, _, Backbone) {
    
    "use strict";
    
    var DiscussionForm = Backbone.View.extend({
        
        el: '#discussion-create-form',
        
        initialize: function () {
            this.$el.find('#id_intro').customCKEditor('custom');
            this.$el.find('#id_latitude').before('<div id="map"></div>');
            this.$el.find('#id_latitude, #id_longitude').css('display', 'none');
            this.$el.find('#map').mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 640,
                height: 480
            });
            this.$el.find('[type="checkbox"]').bootstrapSwitch({
                onText: gettext("Opened"),
                offText: gettext("Closed"),
                wrapperClass: 'form-group',
                onColor: 'success',
                offColor: 'danger'
            });
            this.$el.find('#id_tags').tagsInput({
                autocomplete_url: '/rest/tags/'
            });
        }
    });
    
    return DiscussionForm;
});