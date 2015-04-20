//
// list.js
// =======

// Main comment list view.

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
    this.$el = options.$el;
    this.collection = new CommentCollection();
    this.currentPage = options.currentPage;
    this.textarea = this.$el.find('[name="comment"]');
    this.uri = new CUri(options.url);
    this.uri.add('ct', options.ct);
    this.uri.add('pk', options.pk);
    this.uri.add('page', this.currentPage);
    this.collection.url = this.uri.url();
    _.bindAll(this, "onFetch");
    this.collection.fetch({ success: this.onFetch });
  },

  onFetch: function (collection) {
    this.renderPage(collection.models);
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

  // Render newly created comment

  renderComment: function (item) {
    var model = new CommentModel(item);
    var view = new CommentView({
      model: model
    });
    $(view.render().el)
      .prependTo(this.$el.find('.comments'));
    this.textarea.val('');
  },

  nextPage: function () {
    var _self = this;
    if (!this.collection.hasNext) {
      return;
    }
    this.uri.add('page', ++this.currentPage);
    this.collection.url = this.uri.url();
    this.collection.fetch({ success: this.onFetch });
  },

  addComment: function (e) {
    e.preventDefault();
    cUtils.createComment({
      comment: this.textarea.val(),
      ct: this.$el.attr('data-ct'),
      pk: this.$el.attr('data-pk')
    }, this.collection, this.renderComment, this);
  }
});

return CommentListView;

});
