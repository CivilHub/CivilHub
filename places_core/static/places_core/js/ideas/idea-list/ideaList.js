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
                console.log(that.collection);
                that.render(resp.current_page, resp.total_pages);
            });
        },

        render: function (current_page, total_pages) {
            var that = this;
            this.collection.each(function (item) {
                this.renderEntry(item);
            }, this);
            //~ this.paginator = CivilApp.SimplePaginator({
                //~ currentPage: current_page,
                //~ totalPages: total_pages,
                //~ prevLabel: gettext("Previous"),
                //~ nextLabel: gettext("Next"),
                //~ onChange: function (page) {
                    //~ that.filter(page);
                //~ }
            //~ });
            //~ $(this.paginator.$el).appendTo(this.$el);
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
                console.log(that.collection);
                that.$el.empty();
                that.render(resp.current_page, resp.total_pages);
            });
        }
    });
    
    return IdeaList;
});