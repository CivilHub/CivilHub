//
// pollListView.js
// ===============
// Generic poll list view for selected location.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/polls/poll-list/pollListEntry',
        'js/modules/polls/poll-list/pollListCollection',
        'js/modules/utils/pageable-view',
        'jpaginate'],

function ($, _, Backbone, PollListEntry, PollListCollection, PageableView) {
    
    "use strict";
    
    var PollListView = PageableView.extend({

        initialize: function () {
            this.collection = new PollListCollection();
            this.collection.setPageSize(window.pageSize);
            this.$el.appendTo('#polls');
            this.listenTo(this.collection, 'sync', this.render);
        },

        render: function () {
            var self = this;
            if (this.collection.length) {
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
            } else if (this.filtered !== undefined && this.filtered) {
                this.$el.empty().html($('#no-results-tpl').html());
            } else {
                $('.content-container').hide();
                $('.no-entries').show();
            }
        },

        renderEntry: function (item) {
            var itemView = new PollListEntry({
                    model: item
                });
            $(itemView.render().el).insertBefore(this.$el.find('.page-info'));
        }
    });
    
    return PollListView;
});