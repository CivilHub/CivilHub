//
// news-list.js
// ============
//
// Manage location's blog.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/modules/utils/utils',
        'js/modules/utils/pageable-view',
        'paginator',
        'moment',
        'jpaginate'],

function ($, _, Backbone, utils, PageableView) {

  "use strict";

  var currentLang = window.CivilApp.language || 'en';

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
                .text(moment(this.model.get('date_created'))
                    .lang(currentLang).fromNowOrNow());
            if (this.model.get('edited')) {
              this.$el.find('.date-edited')
                  .text(moment(this.model.get('date_edited'))
                      .lang(currentLang).fromNowOrNow());
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
            return { totalRecords: resp.count };
          }
        }),

        NewsList = PageableView.extend({

          initialize: function () {
            this.collection = new NewsCollection();
            this.collection.setPageSize(window.pageSize);
            this.$el.appendTo('#entries');
            this.listenTo(this.collection, 'sync', this.render);
          },

          render: function () {
            var self = this;
            if (this.collection.length > 0) {
              // It seems that we have something to show
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
              // Show info that there are no items
              $('.content-container').hide();
              $('.no-entries').show();
            }
          },

          renderEntry: function (item) {
            var itemView = new NewsView({
              model: item
            });
            $(itemView.render().el).insertBefore(this.$el.find('.page-info'));
          }
        });

  return NewsList;
});
