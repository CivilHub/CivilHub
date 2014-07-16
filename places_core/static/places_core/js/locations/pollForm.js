//
// pollForm.js
// ===========
//
define(['jquery',
        'underscore',
        'backbone',
        'editor/customCKEditor'],

function ($, _, Backbone) {
    
    "use strict";
    
    var PollForm = Backbone.View.extend({
        
        el: '#poll-create-form',
        
        initialize: function () {
            this.$el.find('#id_question').customCKEditor('custom');
        }
    });
    
    return PollForm;
});