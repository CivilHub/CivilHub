//
// news-list.js
// ============
//
// Manage location's blog.
//
define(['jquery', 'underscore', 'backbone', 'js/utils/utils'],

function ($, _, Backbone, utils) {
    "use strict";
        
    var baseurl = $('#rest-api-url').val(),

        NewsModel = Backbone.Model.extend({}),

        NewsView = Backbone.View.extend({
            tagName: 'div',

            className: 'news-entry',

            template: _.template($('#news-entry-tpl').html()),

            submenu: {},

            events: {
                'click .submenu-toggle': 'openMenu'
            },

            render: function () {
                var that = this;
                this.$el.html(this.template(this.model.toJSON()));
                this.submenu = {
                    $el: that.$el.find('.entry-submenu'),
                    opened: false
                };
                return this;
            },

            openMenu: function () {
                if (this.submenu.opened) {
                    this.submenu.$el.slideUp('fast');
                    this.submenu.opened = false;
                } else {
                    this.submenu.$el.slideDown('fast');
                    this.submenu.opened = true;
                }
            },
        }),

        NewsCollection = Backbone.Collection.extend({
            model: NewsModel,
            url: baseurl
        }),

        NewsList = Backbone.View.extend({
            el: '#entries',

            initialize: function () {
                var that = this;
                $.get(baseurl, function (resp) {
                    that.collection = new NewsCollection(resp.results);
                    that.render(resp.current_page, resp.total_pages);
                });
            },

            render: function (current_page, total_pages) {
                var that = this;
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
                this.paginator = CivilApp.SimplePaginator({
                    currentPage: current_page,
                    totalPages: total_pages,
                    prevLabel: gettext("Previous"),
                    nextLabel: gettext("Next"),
                    onChange: function (page) {
                        that.filter(page);
                    }
                });
                $(this.paginator.$el).appendTo(this.$el);
            },

            renderEntry: function (item) {
                var itemView = new NewsView({
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
                    that.collection = new NewsCollection(resp.results);
                    that.$el.empty();
                    that.render(resp.current_page, resp.total_pages);
                });
            }
        });
    
    return NewsList;
});