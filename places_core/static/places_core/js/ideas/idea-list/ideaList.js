//
// ideaList.js
// ===========
// Main list view.
define(['jquery',
        'underscore',
        'backbone',
        'utils',
        'js/ideas/idea-list/ideaCollection',
        'js/ideas/idea-list/ideaView',
        'js/ui/paginatorView'],

function ($, _, Backbone, utils, IdeaCollection, IdeaView, PaginatorView) {
    "use strict";
    
    var baseurl = $('#rest-api-url').val();
    
    var IdeaList = Backbone.View.extend({
        el: '#idea-list-view',

        initialize: function () {
            var self = this;
            $.get(baseurl, function (resp) {
                if (resp.count) {
                    self.collection = new IdeaCollection(resp.results);
                    self.collection.setPageSize(2);
                    self.render();
                    self.paginator = new PaginatorView(self.collection);
                    $(self.paginator.render().el).insertAfter(self.$el);
                    window.testP = self.paginator;
                } else {
                    self.$el.append('<p class="alert alert-info">' + gettext("There are no ideas yet") + '</p>');
                }
                self.listenTo(self.collection, 'sync', self.render);
            });
        },

        render: function () {
            this.$el.empty();
            this.collection.each(function (item) {
                this.renderEntry(item);
            }, this);
        },

        renderEntry: function (item) {
            var itemView = new IdeaView({
                    model: item
                });
            $(itemView.render().el).appendTo(this.$el);
        },

        filter: function (page) {
            var that = this,
                filters = utils.getListOptions();
                
            _.extend(this.collection.queryParams, filters);
            this.collection.fetch();
            console.log(this.collection);
        }
    });
    
    return IdeaList;
});