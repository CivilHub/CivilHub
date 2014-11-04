//
// discussionList.js
// =================
// Main view for list of discussions.
define(['jquery',
        'underscore',
        'backbone',
        'js/modules/topics/discussion-list/discussionEntry',
        'js/modules/topics/discussion-list/discussionCollection',
        'js/modules/utils/pageable-view',
        'jpaginate'],
        
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
            if (this.collection.length > 0) {
                $('.content-container').addClass('main-content');
                this.$el.empty();
                this.$el.html(this.template(this.collection.state));
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
                this.$el.find('.page').on('click', function () {
                    self.getPage(parseInt($(this).attr('data-index'), 10));
                });
                this.$el.find('.pagination').pagination({
                    defaultOffset: self.collection.state.currentPage,
                    visibleEntries: 9
                });
                $('.custom-label-list').show();
            } else {
                $('.content-container').hide();
                $('.no-entries').show();
            }
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