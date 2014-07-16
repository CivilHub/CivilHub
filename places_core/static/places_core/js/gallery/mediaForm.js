//
// mediaForm.js
// ============
// Formularz uploadowania zdjęć na stronie galerii lokacji.
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    "use strict";
    
    var MediaForm = Backbone.View.extend({
        
        el: '#media-form',
        
        initialize: function () {
            //~ this.$el.find('#id_intro').customCKEditor('custom');
            //~ this.$el.find('#id_latitude').before('<div id="map"></div>');
            //~ this.$el.find('#id_latitude, #id_longitude').css('display', 'none');
            //~ this.$el.find('#map').mapinput({
                //~ latField: '#id_latitude',
                //~ lngField: '#id_longitude',
                //~ width: 640,
                //~ height: 480
            //~ });
            //~ this.$el.find('[type="checkbox"]').bootstrapSwitch({
                //~ onText: gettext("Opened"),
                //~ offText: gettext("Closed"),
                //~ wrapperClass: 'form-group',
                //~ onColor: 'success',
                //~ offColor: 'danger'
            //~ });
            //~ this.$el.find('#id_tags').tagsInput({
                //~ autocomplete_url: '/rest/tags/'
            //~ });
        },
        
        toggle: function () {
            if (this.$el.is(':visible')) {
                this.$el.slideUp('fast');
            } else {
                this.$el.slideDown('fast');
            }
        }
    });
    
    return MediaForm;
});