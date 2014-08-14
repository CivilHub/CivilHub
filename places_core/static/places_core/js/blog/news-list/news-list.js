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
        'paginator',
        'moment'],

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
                this.$el.find('.date-created')
                    .text(moment(this.model.get('date_created')).fromNow());
                if (this.model.get('edited')) {
                    this.$el.find('.date-edited')
                        .text(moment(this.model.get('date_edited')).fromNow());
                }
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
            
            queryParams: {
                totalRecords: 'count'
            },
            
            parseRecords: function (data) {
                return data.results;
            },
            
            parseState: function (resp, queryParams, state, options) {
                return {totalRecords: resp.count};
            }
        }),

        NewsList = Backbone.View.extend({
            el: '#entries',

            initialize: function () {
                var self = this;
                $.get(baseurl, function (resp) {
                    if (resp.count) {
                        self.collection = new NewsCollection(resp.results);
                        self.collection.setPageSize(2);
                        self.render();
                        self.paginator = new PaginatorView(self.collection);
                        setTimeout(function () {
                            $(self.paginator.render().el).insertAfter(self.$el);
                        }, 500);
                    } else {
                        self.$el.append('<p class="alert alert-info">' + gettext("There are no entries yet") + '</p>');
                    }
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
                    filters = utils.getListOptions();
                    
                filters.page = 1;
                _.extend(this.collection.queryParams, filters);
                this.collection.fetch();
                this.paginator.render();
            }
        });
    
    return NewsList;
});