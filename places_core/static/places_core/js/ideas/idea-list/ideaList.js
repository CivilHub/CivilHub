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
                    self.render();
                    self.paginator = new PaginatorView({
                        count: resp.count,
                        perPage: 2,
                        targetCollection: self.collection
                    });
                    $(self.paginator.render().el).insertAfter(self.$el);
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
                filters = utils.getListOptions(),
                url = baseurl + '&' + utils.JSONtoUrl(filters);
            this.collection.url = url;
            this.collection.fetch();
        }
    });
    
    return IdeaList;
});