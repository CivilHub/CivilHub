//
// locationForm.js
// ===============
//
define(['jquery',
        'underscore',
        'backbone',
        'js/editor/customCKEditor',
        'tagsinput'],

function ($, _, Backbone) {
    
    "use strict";
    
    var NewsForm = Backbone.View.extend({
        el:  "#news-create-form",
        
        initialize: function () {
            this.$el.find('#id_content').customCKEditor();
            this.$el.find('#id_tags').tagsInput({
                autocomplete_url: '/rest/tags/'
            });
        }
    });
    
    return NewsForm;
});