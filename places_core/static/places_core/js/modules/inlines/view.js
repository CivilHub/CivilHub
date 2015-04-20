//
// view.js
// =======

// View for single comment entry.

define(['jquery',
        'underscore',
        'backbone',
        'CUri',
        'js/modules/ui/ui',
        'js/modules/utils/utils',
        'js/modules/inlines/utils',
        'js/modules/inlines/model',
        'js/modules/inlines/collection',
        'text!js/modules/inlines/templates/comment.html',
        'text!js/modules/inlines/templates/edit_form.html'],

function ($, _, Backbone, CUri, ui, utils, cUtils, CommentModel, CommentCollection, html, form) {

"use strict";

function sendVote (id, vote, callback, context) {
  var data = {
    csrfmiddlewaretoken: utils.getCookie('csrftoken'),
    vote: vote
  };
  $.post('/api-comments/list/' + id + '/vote/', data,
    function (response) {
      ui.message.addMessage(response.message, response.status);
      callback.call(context, response, vote);
    }
  );
}

var CommentView = Backbone.View.extend({

  tagName: 'div',

  className: 'comment',

  template: _.template(html),

  editFormTemplate: _.template(form),

  // Flag - edit form opened
  edited: false,

  // Flag - reply form opened
  replied: false,

  events: {
    'click .vote-link': 'vote',
    'click .comment-edit': 'toggleEdit',
    'click .comment-reply': 'toggleReplyForm',
    'click .show-replies': 'toggleReplies'
  },

  initialize: function () {
    _.bindAll(this, 'updateCounter', 'onFetch');
    this.model.on('change', this.render, this);
    this.collection = new CommentCollection();
    this.uri = new CUri('/api-comments/list/');
    this.uri.add('parent', this.model.get('id'));
    this.collection.url = this.uri.url();
    if (this.model.get('answers') > 0) {
      this.collection.fetch({ success: this.onFetch });
    }
  },

  onFetch: function (collection) {
    this.renderPage(collection.models);
  },

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    this.$counter = this.$el.find('.comment-total-votes');
    this.votes = parseInt(this.$counter.text(), 10);
    if (isNaN(this.votes)) {
      this.votes = 0;
    }
    this.$replyForm = this.$el.find('.reply-form');
    this.$replyForm.find('.btn-cancel-comment').on('click', function (e) {
      e.preventDefault();
      this.$replyForm.toggle();
    }.bind(this));
    this.$replyForm.find('.btn-submit-comment').on('click', function (e) {
      e.preventDefault();
      this.addReply();
    }.bind(this));
    return this;
  },

  update: function (comment) {
    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", utils.getCookie('csrftoken'));
      }
    });
    this.model.set('comment', comment);
    this.model.url = '/api-comments/list/' + this.model.get('id') + '/';
    this.model.save({ comment: comment }, { patch: true });
  },

  vote: function (e) {
    var vote = false;
    if ($(e.currentTarget).hasClass('vote-up-link')) {
      vote = true;
    }
    var data = {
      csrfmiddlewaretoken: utils.getCookie('csrftoken'),
      vote: vote
    };
    e.preventDefault();
    sendVote(this.model.get('id'), vote, this.updateCounter, this);
  },

  updateCounter: function (response, vote) {
    if (response.created) {
      if (vote) {
        this.$counter.text(++this.votes);
      } else {
        this.$counter.text(--this.votes);
      }
    }
  },

  // Edition form

  opendEdit: function () {
    var $form = this.editFormTemplate(this.model.toJSON());
    this.$el.find('.comment-content').hide().after($form);
    this.$el.find('.btn-cancel-comment').on('click', function (e) {
      e.preventDefault();
      this.closeEdit();
    }.bind(this));
    this.$el.find('.btn-submit-comment').on('click', function (e) {
      e.preventDefault();
      this.update($('#comment').val());
      this.closeEdit();
    }.bind(this));
    this.edited = true;
  },

  closeEdit: function () {
    this.$el.find('.comment-form-body').empty().remove();
    this.$el.find('.comment-content').show();
    this.edited = false;
  },

  toggleEdit: function (e) {
    e.preventDefault();
    if (this.edited) {
      this.closeEdit();
    } else {
      this.opendEdit();
    }
  },

  // Answers

  renderPage: function (comments) {
    _.each(comments, function (comment) {
      var view = new CommentView({
        model: comment
      });
      $(view.render().el)
        .appendTo(this.$el.find('.subcomments'));
    }, this);
  },

  renderReply: function (reply) {
    var view = new CommentView({
      model: new CommentModel(reply)
    });
    $(view.render().el).prependTo(this.$el.find('.subcomments'));
    this.$replyForm.find('textarea:first').val('');
  },

  addReply: function () {
    cUtils.createComment({
      comment: this.$replyForm.find('textarea:first').val(),
      ct: this.model.get('content_type'),
      pk: this.model.get('object_pk'),
      parent: this.model.get('id')
    }, this.collection, this.renderReply, this);
  },

  toggleReplies: function (e) {
    e.preventDefault();
    this.$el.find('.subcomments').slideToggle('fast');
  },

  toggleReplyForm: function (e) {
    e.preventDefault();
    this.$el.find('.reply-form').toggle();
  }
});

return CommentView;

});
