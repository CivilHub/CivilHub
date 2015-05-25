//
// comment-list-view.js
// ====================

// Główny widok dla komentarzy - obsługuje całą listę.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/utils/utils',
        'js/modules/comments/comment-collection',
        'js/modules/comments/comment-view',
        'js/modules/comments/comment-model'],

function ($, _, Backbone, utils, CommentCollection, CommentView, CommentModel) {

"use strict";

function incrementCommentCount () {
  var value = parseInt($('.comment-count').text(), 10);
  $('.comment-count').text((_.isNaN(value)) ? 1 : ++value);
}

var CommentListView = Backbone.View.extend({

  el: '#comments',

  // References to comments views. They both share the same key - ID model.
  items: {},
  
  initialize: function (options) {
    
    var self = this; // FIXME: delete this
    
    // Necessary due to Django CSRF Protection
    $.ajaxSetup({
      headers: { 'X-CSRFToken': utils.getCookie('csrftoken') }
    });
    
    // Evocation of a paginable collection, setting the number of elements
    // on one site and displaying the first one.
    this.collection = new CommentCollection(options);
    this.collection.state.pageSize = window.pageSize;
    this.collection.fetch({
      success: function () {
        self.render();
      }
    });
    
    // Adding new commnets (unnested)
    $('#user-comment-form').on('submit', function (e) {
      e.preventDefault();
      this.addComment();
    }.bind(this));
    
    // We delete the view references when we restart the collection/load a new one
    this.listenTo(this.collection, 'sync', this.cleanup);
  },
  
  render: function () {
    // Displays a list of comments.
    this.collection.each(function (item) {
      this.renderComment(item);
    }, this);
    // Off and on are complusory here due to later list loading problems
    // Enable lazdy-loading on page scrolling
    $(window).off('scroll');
    $(window).scroll(function () {
      if ($(window).scrollTop() + $(window).height() == $(document).height()) {
        this.nextPage();
      }
    }.bind(this));
  },
  
  renderComment: function (item) {
    // This function adds comments at the end of the list,
    // it is used during inicialization and reset of collection
    var comment = new CommentView({ model:item });
    comment.parentView = this;
    $(comment.render().el).appendTo(this.$el);
    this.items[item.get('id')] = comment;
  },
  
  prependComment: function (item) {
    // This function adds comments at the beginning of the list, e.g. when we
    // create a new one.
    var comment = new CommentView({ model:item });
    $(comment.render().el).prependTo(this.$el);
  },
  
  addComment: function () {
    var self = this; // FIXME: pozbyć się tego
    if ($('#comment').val().length <= 0) {
      alert(gettext("Comment cannot be empty"));
      return false;
    }
    // Creation of a new comment - from the from we download
    // only the text, the rest is added through scripts
    // and the server. 
    var newComment = {
      comment: $('#comment').val(),
      content_type: $('#target-type').val(),
      content_id: $('#target-id').val(),
      username: $('#target-user').val(),
      user_full_name: $('#target-user-fullname').val(),
      avatar: $('#target-avatar').val(),
    }
    this.collection.create(newComment, {
      success: function (model, resp) {
        self.prependComment(model);
      }
    });
    // Clear the form
    $('#comment').val('');
    // Increase the number of comments in the information window
    incrementCommentCount();
  },
  
  filter: function (filter) {
    var self = this;
    // Reset
    this.$el.empty();
    // We use one of the filters: 'votes', 'submit_date', '-submit_date'/
    this.collection.state.currentPage = 1;
    _.extend(this.collection.queryParams, {
      filter: filter
    });
    this.collection.fetch({
      success: function () {
        self.render();
      }
    });
  },
  
  nextPage: function () {
    // We download the next page after scrolling. This function
    // sometimes throws an error or returns a 404, you shouldn't 
    // wory about it :)
    // Backbone.pageableCollection has some sort of an error that
    // makes hasNextPage useless.
    var self = this,
    model = null;
    
    this.collection.getNextPage({
      // We download a new site and display the comments.
      success: function (collection, response, method) {
        _.each(response.results, function (item) {
          var model = new CommentModel(item);
          self.renderComment(model);
        });
      }
    });
  },
  
  cleanup: function () {
    // This method clear the list of views connected with the models in order
    // Metoda "czyści" listę widoków powiązanych z modelami w kolekjci
    this.items = {};
  }
});

return CommentListView;

});
