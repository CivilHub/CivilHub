//
// news-list.js
// ============
//
// Manage location's blog.
//
define(['jquery',
        'underscore',
        'backbone',
        'utils', 
        'js/ui/paginatorView',
        'paginator'],

function ($, _, Backbone, utils, PaginatorView) {
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

        NewsCollection = Backbone.PageableCollection.extend({
            
            model: NewsModel,
            
            url: baseurl,
            
            parse: function (data) {
                return data.results;
            }
        }),

        NewsList = Backbone.View.extend({
            el: '#entries',

            initialize: function () {
                var self = this;
                $.get(baseurl, function (resp) {
                    self.collection = new NewsCollection(resp.results);
                    self.render();
                    self.paginator = new PaginatorView({
                        count: resp.count,
                        perPage: 2,
                        targetCollection: self.collection
                    });
                    $(self.paginator.render().el).insertAfter(self.$el);
                    self.listenTo(self.collection, 'sync', self.render);
                });
            },

            render: function (current_page, total_pages) {
                var that = this;
                this.$el.empty();
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
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
                    that.render();
                });
            }
        });
    
    return NewsList;
});