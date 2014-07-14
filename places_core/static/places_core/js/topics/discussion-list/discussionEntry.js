//
// discussionEntry.js
// ==================
// Single list entry view.
define(['jquery', 'underscore', 'backbone'],

function ($, _, Backbone) {
    "use strict";
    
    var DiscussionEntry = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'topic-list-entry custom-list-entry',
        
        template: _.template($('#topic-entry').html()),
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
    return DiscussionEntry;
});