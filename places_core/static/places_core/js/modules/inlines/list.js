//
// list.js
// =======

// Main comment list view. Manage list of comments for selected item. View
// instances should be created by external scripts. You have to pass options
// to constructor in plain object, containing at least DOM element for which
// comment list should be created. See comment_tags.py for details of html
// structure for plugin and required data attributes.

// FIXME: avoid model duplication when fetching new page.

define(['jquery',
        'underscore',
        'backbone',
        'CUri',
        'js/modules/inlines/model',
        'js/modules/inlines/collection',
        'js/modules/inlines/view',
        'js/modules/inlines/utils'],

function ($, _, Backbone, CUri, CommentModel, CommentCollection, CommentView, cUtils) {

"use strict";

function fetchData(url, callback, context) {
  $.get(url, function (response) {
    callback.call(context, response);
  });
}

var CommentListView = Backbone.View.extend({

  events: {
    'click .add-comment': 'addComment'
  },

  initialize: function (options) {

    // This option is required - we need some DOM element to operate on.

    this.$el = options.$el;

    // Set inner counter so that we don't have to rely on DOM context
    // to get numbers as this may be confusing and inaccurate.

    this.$counter = options.$counter || this.$('.comment-count');
    this.count = parseInt(this.$el.attr('data-count'), 10);
    if (isNaN(this.count)) {
      this.count = 0;
    }

    // Main input to create new comment.

    this.textarea = this.$el.find('[name="comment"]');

    // Create collection and set page to (by default) 1. We use CUri here, so
    // that params may be passed only once and THEN appended to collection URL.

    this.collection = new CommentCollection();
    this.currentPage = options.currentPage;
    this.uri = new CUri(options.url);
    this.uri.add('ct', options.ct);
    this.uri.add('pk', options.pk);
    this.uri.add('page', this.currentPage);
    this.collection.url = options.url;

    // Allow list filtering by date/votes.

    this.$el.find('.filters').find('a').on('click', function (e) {
      e.preventDefault();
      this.filter($(e.currentTarget).attr('data-order'));
    }.bind(this));

    // Render single items as they are added to collection.

    this.listenTo(this.collection, 'add', this.renderComment);
    this.listenTo(this.collection, 'reset', this.renderPage);
  },

  // Wrapper for collection's fetch function. Useful for scripts on static
  // content pages, when we have to fetch collection on init.

  fetch: function () {
    this.collection.fetch({ data: this.uri.params });
  },

  // Trigger when some filter is selected. Resets
  // entire collection in different order.

  filter: function (filter) {
    this.$el.find('.comments').empty();
    this.currentPage = 1;
    this.uri.add('page', this.currentPage);
    this.uri.add('o', filter);
    fetchData(this.uri.url(), function (response) {
      // FIXME: not rendering when filtered list is on last page.
      this.collection.reset(response.results);
      this.collection.nextUrl = response.next;
      this.collection.hasNext = !_.isNull(response.next);
    }, this);
  },

  renderPage: function () {
    this.collection.each(function (item) {
      this.renderComment(item);
    }, this);
  },

  // Render newly created comment. Append fetched items and prepend
  // new comments on top of the list.

  renderComment: function (item) {
    var view = new CommentView({
      model: item
    });
    var $area = this.$('.comments:first');
    var $el = $(view.render().el);
    if (this.collection.indexOf(item) === 0) {
      $el.prependTo($area);
    } else {
      $el.appendTo($area);
    }

    //Resize textarea
    $.each($('textarea'), function() {
      var offset = this.offsetHeight - this.clientHeight;
      var resizeTextarea = function(el) {
        $(el).css('height', 'auto').css('height', el.scrollHeight + offset);
      };
      $(this).on('keyup input', function() { resizeTextarea(this); });
    });

    this.textarea.val('');
    if (!this.collection.hasNext) {
      this.$('.show-more').hide();
    } else {
      this.$('.show-more').show();
    }
  },

  // Create new comment in database.

  addComment: function (e) {
    e.preventDefault();
    cUtils.createComment({
      comment: this.textarea.val(),
      ct: this.$el.attr('data-ct'),
      pk: this.$el.attr('data-pk')
    }, this.collection, this.insert, this);
    this.updateCounter();
  },

  // Inserts new element to collection. This allows us to use external
  // function for model creation instead of collection.create method.

  insert: function (data) {
    var m = this.collection.push(data, { at: 0 });
  },

  // Update current number of comments for commented object.

  updateCounter: function () {
    this.$counter.text(++this.count);
  },

  // Get next comment page. Use this on scroll or when
  // user clicks 'next' button.

  nextPage: function () {
    var _self = this;
    if (!this.collection.hasNext) {
      return;
    }
    this.uri.add('page', ++this.currentPage);
    fetchData(this.uri.url(), function (response) {
      this.collection.set(response.results, { remove: false });
      this.collection.hasNext = response.next;
    }, this);
  }
});

return CommentListView;

});
