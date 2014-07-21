//
// pollForm.js
// ===========
//
define(['jquery',
        'underscore',
        'backbone',
        'tagsinput',
        'js/editor/customCKEditor'],

function ($, _, Backbone) {
    
    "use strict";
    
    var PollForm = Backbone.View.extend({
        
        el: '#poll-create-form',
        
        initialize: function () {
            this.$el.find('#id_question').customCKEditor('custom');
            this.$el.find('#id_tags').tagsInput({
                autocomplete_url: '/rest/tags/'
            });
        }
    });
    
    return PollForm;
});