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
    'click .vote-up-link:first': 'vote',
    'click .vote-down-link:first': 'vote',
    'click .comment-edit:first': 'toggleEdit',
    'click .comment-reply:first': 'toggleReplyForm',
    'click .show-replies:first': 'toggleReplies'
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
    this.$replyForm.find('.btn-cancel-comment:first').on('click', function (e) {
      e.preventDefault();
      this.$replyForm.toggle();
    }.bind(this));
    this.$replyForm.find('.btn-submit-comment:first').on('click', function (e) {
      e.preventDefault();
      this.addReply();
    }.bind(this));

    // NGO members
    var ngo = this.model.get('author').organizations;
    if (!_.isUndefined(ngo) && ngo.count > 0) {
      $('<div class="ngo-badge-group"><div class="fa fa-bank"></div></div>')
        .insertAfter(this.$('.comment-author-avatar:first'));
      _.each(ngo.items, function (item) {
        this.renderBadge(item);
      }, this);
    }

    return this;
  },

  renderBadge: function (ngo) {
    var html = ([
      '<a href="', ngo.url,
      '"><span class="badge badge-green badge-btn comment-badge">',
      ngo.name, '</span></a>'
    ]).join('');
    $(html).insertAfter(this.$el.find('.comment-date-from-now:first'));
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
    this.$el.find('.comment-content:first').hide().after($form);
    this.$el.find('.btn-cancel-comment:first').on('click', function (e) {
      e.preventDefault();
      this.closeEdit();
    }.bind(this));
    this.$el.find('.btn-submit-comment:first').on('click', function (e) {
      e.preventDefault();
      this.update(this.$('.update-comment:first').val());
      this.closeEdit();
    }.bind(this));
    this.edited = true;
  },

  closeEdit: function () {
    this.$('.comment-update-form:first').empty().remove();
    this.$('.comment-content:first').show();
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
        .appendTo(this.$el.find('.subcomments:first'));
    }, this);
  },

  renderReply: function (reply) {
    var view = new CommentView({
      model: new CommentModel(reply)
    });
    $(view.render().el).prependTo(this.$el.find('.subcomments:first'));
    this.$replyForm.find('textarea:first').val('');
  },

  addReply: function () {
    cUtils.createComment({
      comment: this.$replyForm.find('textarea:first').val(),
      ct: this.model.get('content_type'),
      pk: this.model.get('object_pk'),
      parent: this.model.get('id')
    }, this.collection, this.renderReply, this);
    this.toggleReplyForm();
  },

  toggleReplies: function (e) {
    e.preventDefault();
    this.$('.subcomments:first').slideToggle('fast');
  },

  toggleReplyForm: function (e) {
    if (!_.isUndefined(e)) {
      e.preventDefault();
    }
    this.$('.comment-form-body:first').toggle();
  }
});

return CommentView;

});
