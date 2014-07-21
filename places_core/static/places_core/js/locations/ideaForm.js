//
// discussionForm.js
// =================
//
define(['jquery',
        'underscore',
        'backbone',
        'js/editor/customCKEditor',
        'tagsinput'],

function ($, _, Backbone) {
    
    "use strict";
    
    var IdeaForm = Backbone.View.extend({
        
        el: '#idea-create-form',
        
        initialize: function () {
            this.$el.find('#id_description').customCKEditor('custom');
            this.$el.find('#id_tags').tagsInput({
                autocomplete_url: '/rest/tags/'
            });
        }
    });
    
    return IdeaForm;
});