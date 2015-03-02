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

        initialize: function (opts) {
            this.collection = new DiscussionCollection();
            this.$el.appendTo('#discussions');
            this.listenTo(this.collection, 'sync', this.render);
            if (opts.cat !== null) {
                this.filtered = true;
                _.extend(this.collection.queryParams, {category: opts.cat});
            }
            this.collection.setPageSize(window.pageSize);
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
            } else if (this.filtered !== undefined && this.filtered) {
                $('.custom-label-list').show();
                this.$el.empty().html($('#no-results-tpl').html());
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