//
// discussionList.js
// =================
// Main view for list of discussions.
define(['jquery',
        'underscore',
        'backbone',
        'js/topics/discussion-list/discussionEntry',
        'js/topics/discussion-list/discussionCollection',
        'js/utils/pageable-view'],
        
function ($, _, Backbone, DiscussionEntry, DiscussionCollection, PageableView) {
    
    "use strict";
    
    var DiscussionList = PageableView.extend({

        initialize: function () {
            this.collection = new DiscussionCollection();
            this.collection.setPageSize(window.pageSize);
            this.$el.appendTo('#discussions');
            this.listenTo(this.collection, 'sync', this.render);
        },

        render: function () {
            var self = this;
            this.$el.empty();
            this.$el.html(this.template(this.collection.state));
            this.collection.each(function (item) {
                this.renderEntry(item);
            }, this);
            this.$el.find('.page').on('click', function () {
                self.getPage(parseInt($(this).attr('data-index'), 10));
            });
        },

        renderEntry: function (item) {
            var itemView = new DiscussionEntry({
                    model: item
                });
            $(itemView.render().el).insertBefore(this.$el.find('.page-info'));
        }
    });
    
    return DiscussionList;
});