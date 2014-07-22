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