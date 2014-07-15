//
// ideaList.js
// ===========
// Main list view.
define(['jquery',
        'underscore',
        'backbone',
        'js/utils/utils',
        'js/ideas/idea-list/ideaCollection',
        'js/ideas/idea-list/ideaView'],

function ($, _, Backbone, utils, IdeaCollection, IdeaView) {
    "use strict";
    
    var baseurl = $('#rest-api-url').val();
    
    var IdeaList = Backbone.View.extend({
        el: '#idea-list-view',

        initialize: function () {
            var that = this;
            $.get(baseurl, function (resp) {
                that.collection = new IdeaCollection(resp.results);
                that.render();
            });
        },

        render: function () {
            var that = this;
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
                url  = baseurl + '&' + utils.JSONtoUrl(filters);
            if (page) url += '&page=' + page;
            $.get(url, function (resp) {
                that.collection = new IdeaCollection(resp.results);
                that.$el.empty();
                that.render();
            });
        }
    });
    
    return IdeaList;
});