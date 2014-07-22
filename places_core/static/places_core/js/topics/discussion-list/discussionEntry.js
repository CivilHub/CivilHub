//
// discussionEntry.js
// ==================
// Single list entry view.
define(['jquery', 'underscore', 'backbone', 'moment'],

function ($, _, Backbone) {
    "use strict";
    
    var DiscussionEntry = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'topic-list-entry custom-list-entry',
        
        template: _.template($('#topic-entry').html()),
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            this.$el.find('.date-created')
                .text(moment(this.model.get('date_created')).fromNow());
            if (this.model.get('edited')) {
                this.$el.find('.date-edited')
                    .text(moment(this.model.get('date_edited')).fromNow());
            }
            return this;
        }
    });
    
    return DiscussionEntry;
});