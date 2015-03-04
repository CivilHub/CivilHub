//
// ideaList.js
// ===========
// Main list view. Dziedziczy z modelu 'PageableView'.
define(['jquery',
        'underscore',
        'backbone',
        'js/modules/ideas/idea-list/ideaCollection',
        'js/modules/ideas/idea-list/ideaView',
        'js/modules/utils/pageable-view',
        'jpaginate'],

function ($, _, Backbone, IdeaCollection, IdeaView, PageableView) {
    
    "use strict";
    
    var IdeaList = PageableView.extend({

        initialize: function () {
            this.collection = new IdeaCollection();
            this.collection.setPageSize(window.pageSize);
            _.extend(this.collection.queryParams, {'per_page': 5});
            this.$el.appendTo('#idea-list-view');
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
            } else if (this.filtered !== undefined && this.filtered) {
                this.$el.empty().html($('#no-results-tpl').html());
            } else {
                $('.content-container').hide();
                $('.no-entries').show();
            }
        },

        renderEntry: function (item) {
            var itemView = new IdeaView({
                    model: item
                });
            $(itemView.render().el).insertBefore(this.$el.find('.page-info'));
        }
    });
    
    return IdeaList;
});