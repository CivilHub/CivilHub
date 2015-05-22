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
    this.collection.url = this.uri.url();

    // Bind inner object methods to value of 'this'. This methods are usually
    // invoked in other context (such as click events) so we need to fixed
    // that behavior.
    _.bindAll(this, "onFetch");

    // Allow list filtering by date/votes.
    this.$el.find('.filters').find('a').on('click', function (e) {
      e.preventDefault();
      this.filter($(e.currentTarget).attr('data-order'));
    }.bind(this));
  },

  // Wrapper for collection's fetch function. Useful for scripts on static
  // content pages, when we have to fetch collection on init.

  fetch: function () {
    this.collection.fetch({ success: this.onFetch });
  },

  // Callback to use when new page of comments is fetched. Putting this into
  // it's own function allows us to use bindAll for 'this' binding.

  onFetch: function (collection) {
    this.renderPage(collection.models);
  },

  // Trigger when some filter is selected. Resets
  // entire collection in different order.

  filter: function (filter) {
    this.$el.find('.comments').empty();
    this.currentPage = 1;
    this.uri.add('page', this.currentPage);
    this.uri.add('o', filter);
    this.collection.url = this.uri.url();
    this.fetch();
  },

  // Render entire page of comments. We use this method
  // after fetching initial collection and every next page.

  renderPage: function (comments) {
    _.each(comments, function (comment) {
      var view = new CommentView({ model: comment });
      $(view.render().el)
        .appendTo(this.$el.find('.comments'));
    }, this);
  },

  // Render newly created comment and prepend it's view to list.

  renderComment: function (item) {
    var model = new CommentModel(item);
    var view = new CommentView({
      model: model
    });
    $(view.render().el)
      .prependTo(this.$el.find('.comments'));
    this.textarea.val('');
  },

  // Create new comment in database.

  addComment: function (e) {
    e.preventDefault();
    cUtils.createComment({
      comment: this.textarea.val(),
      ct: this.$el.attr('data-ct'),
      pk: this.$el.attr('data-pk')
    }, this.collection, this.renderComment, this);
    this.updateCounter();
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
    this.collection.url = this.uri.url();
    this.collection.fetch({
      merge: true,
      success: this.onFetch
    });
  }
});

return CommentListView;

});
