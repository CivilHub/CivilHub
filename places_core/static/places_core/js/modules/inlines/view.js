//
// view.js
// =======

// View for single comment entry.

define(['jquery',
        'underscore',
        'backbone',
        'CUri',
        'js/modules/moment',
        'js/modules/ui/ui',
        'js/modules/utils/utils',
        'js/modules/utils/abuse-window',
        'js/modules/inlines/utils',
        'js/modules/inlines/model',
        'js/modules/inlines/collection',
        'js/modules/inlines/vote-summary',
        'js/modules/inlines/reason',
        'text!js/modules/inlines/templates/comment.html',
        'text!js/modules/inlines/templates/comment_removed.html',
        'text!js/modules/inlines/templates/edit_form.html',
        'bootbox'],

function ($, _, Backbone, CUri, moment, ui, utils, AbuseWindow, cUtils, CommentModel,
          CommentCollection, VoteSummary, ReasonForm, html, altHtml, form) {

"use strict";

// Global to hold our summary window instance.

var summaryWindow = null;

// Globals for moderators

var moderatorForm = null;

// Holds timeout value to smoothly open new vote summary.

var clock = null;

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

function delay (timeout, fn, context) {
  return setTimeout(function () {
    if (_.isFunction(fn)) {
      fn.call(context);
    }
  }, timeout);
}

function confirm (message, fn, context) {
  bootbox.confirm(message, function (r) {
    if (r && _.isFunction(fn)) {
      fn.call(context);
    }
  });
}

moment.fn.fromNowOrNow = function (a) {
  if (moment().diff(this) < 0) {
    return gettext('just now');
  }
  return this.fromNow(a);
};

var CommentView = Backbone.View.extend({

  tagName: 'div',

  className: 'comment',

  template: _.template(html),

  altTemplate: _.template(altHtml),

  editFormTemplate: _.template(form),

  // Flag - edit form opened

  edited: false,

  // Flag - reply form opened

  replied: false,

  events: {
    'click .comment-reply:first': 'toggleReplyForm',
    'click .show-replies:first': 'toggleReplies',
    'click .report-abuse-link': 'report'
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
    var params = this.model.toJSON();
    params.submit_date = moment(params.submit_date).fromNowOrNow();
    this.$el.html(this.getTemplate(params));
    this.$counter = this.$el.find('.comment-total-votes:first');
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

    // Bind content element to avoid problems with edit form

    this.$content = this.$('#content-' + this.model.get('id'));

    this.$('.comment-edit:first').on('click', function (e) {
      this.toggleEdit(e);
    }.bind(this));

    // NGO members

    var ngo = this.model.get('author').organizations;
    if (!_.isUndefined(ngo) && ngo.count > 0) {
      $('<div class="ngo-badge-group"><div class="fa fa-bank text-green"></div></div>')
        .insertAfter(this.$('.comment-author-avatar:first'));
      _.each(ngo.items, function (item) {
        this.renderBadge(item);
      }, this);
    }

    // Enable voting

    this.$('.vote-link').on('click', this.vote.bind(this));

    // Vote summary window

    this.$('.vote-link').on('mouseover', function (e) {
      clock = delay(500, function () {
        this.voteSummary(e);
      }, this);
      $(e.currentTarget).one('mouseout', function (e) {
        clearTimeout(clock);
      });
    }.bind(this));

    // For moderators only - flag comment as removed

    this.$('.comment-moderate').on('click', function (e) {
      e.preventDefault();
      this.moderatorForm({ x: e.pageX - 20, y: e.pageY + 5 });
    }.bind(this));

    this.$('.show-more').on('click', function (e) {
      e.preventDefault();
      $(this).next('.comment-reason').slideToggle('fast');
    });

    // Remove button

    this.$('.comment-remove').on('click', function (e) {
      e.preventDefault();
      this.remove();
    }.bind(this));

    return this;
  },

  getTemplate: function (data) {
    return this.model.get('is_removed') ? this.altTemplate(data)
                                        : this.template(data);
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

  // Votes

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

  voteSummary: function (e) {
    e.stopPropagation();
    var vote = $(e.currentTarget).attr('data-vote');
    if (!_.isUndefined(summaryWindow) && !_.isNull(summaryWindow)) {
      summaryWindow.destroy();
    }
    summaryWindow = new VoteSummary({
      data: {
        id: this.model.get('id'),
        vote: vote
      },
      position: { left: e.pageX - 20, top: e.pageY + 5 }
    });
  },

  // Moderator options

  moderatorForm: function (position) {
    if (!_.isUndefined(summaryWindow) && !_.isNull(summaryWindow)) {
      summaryWindow.destroy();
    }
    if (this.model.get('is_removed')) {
      this.model.flag();
      this.collection.fetch({ success: this.onFetch });
      return;
    }
    moderatorForm = new ReasonForm({
      position: { left: position.x, top: position.y },
      context: this,
      onSelect: function (val) {
        this.model.flag(val);
        this.collection.fetch({ success: this.onFetch });
      }
    });
  },

  report: function (e) {
    e.preventDefault();
    var w = new AbuseWindow(
      CivilApp.contentTypes.comments_customcomment,
      this.model.get('id')
    );
  },

  remove: function () {
    confirm(gettext("Are you sure") + '?', function () {
      this.$el.fadeOut('slow', function () {
        this.model.destroy();
        this.$el.empty().remove();
      }.bind(this));
    }, this);
  },

  // Edition form

  opendEdit: function () {
    var $form = $(this.editFormTemplate(this.model.toJSON()));
    this.$content.hide().after($form);
    $form.find('.btn-cancel-comment:first').on('click', function (e) {
      e.preventDefault();
      this.closeEdit();
    }.bind(this));
    $form.find('.btn-submit-comment:first').on('click', function (e) {
      e.preventDefault();
      this.update(this.$('.update-comment:first').val());
      this.closeEdit();
    }.bind(this));
    this.edited = true;
  },

  closeEdit: function () {
    this.$('.comment-update-form:first').empty().remove();
    this.$content.show();
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

    // This should be comment view method. Sets selected comment to help
    // us create absolute urls for single comments.

    var currentID = window.location.href.split('#')[1] || 'content-0';
    if (!_.isUndefined(currentID)) {
      currentID = parseInt(currentID.replace(/content-/g, ''), 10);
    }
    _.each(comments, function (comment) {
      var view = new CommentView({
        model: comment
      });
      var $el = $(view.render().el);
      $el.appendTo(this.$el.find('.subcomments:first'));
      if (currentID === comment.get('id')) {
        $el.addClass('selected');
        $('html, body').animate({
          scrollTop: $el.offset().top
        }, 1000);
      }
    }, this);
  },

  renderReply: function (reply) {
    var view = new CommentView({
      model: new CommentModel(reply)
    });
    var $el = $(view.render().el);
    $el.prependTo(this.$el.find('.subcomments:first'));
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
