//
// comment-view.js
// ===============

// A single comment view

define(['jquery',
    'underscore',
    'backbone',
    'js/modules/utils/abuse-window',
    'js/modules/comments/comment-model',
    'js/modules/comments/subcomment-collection'],

function ($, _, Backbone, AbuseWindow, CommentModel, SubcommentCollection) {

"use strict";

var currentLang = CivilApp.language;

var CommentView = Backbone.View.extend({

  tagName: 'div',

  className: 'comment container-fluid p-reset',

  template: _.template($('#comment-template').html()),

  initialize: function () {
    var url = '/rest/comments/' + this.model.get('id') + '/replies/';
    $.get(url, function (resp) {
      this.collection = new SubcommentCollection(resp);
      this.renderReplies();
    }.bind(this));
  },

  render: function () {

    // Displays the current comment
    this.$el.html(this.template(this.model.toJSON()));

    // adds a tooltip for voting under each comment
    // Yes, but why before this element is created? :)
    $('.comment-meta-options').find('a').tooltip();

    // Vote YES
    this.$el.find('.vote-up-link').click(function (e) {
      e.preventDefault();
      this.voteUp();
    }.bind(this));

    // Vote NO
    this.$el.find('.vote-down-link').click(function (e) {
      e.preventDefault();
      this.voteDown();
    }.bind(this));

    // Reply to a comment
    this.$el.find('.comment-reply').on('click', function (e) {
      e.preventDefault();
      this.replyComment();
    }.bind(this));

    // Show/hide answers to this comment
    this.$el.find('.show-replies').on('click', function (e) {
      e.preventDefault();
      if (this.collection.length) {
        this.toggleReplies();
      } else {
        return false;
      }
    }.bind(this));

    // Show/hide controlls
    this.$ctrls = this.$el.find('.comment-controls:first');
    this.$el.on('mouseover', function (e) {
      e.stopPropagation();
      this.$ctrls.animate({ opacity:1 }, {
        duration: 'fast',
        queue: false,
        stop: true
      });
    }.bind(this));
    this.$el.on('mouseout', function (e) {
      e.stopPropagation();
      this.$ctrls.animate({ opacity:0 }, {
        duration: 'fast',
        queue: false,
        stop: true
      });
    }.bind(this));

    // Edition of an existing comment
    if (this.$ctrls.find('.comment-edit').length > 0) {
      this.$ctrls.find('.comment-edit').on('click', function (e) {
        e.preventDefault();
        this.editComment();
      }.bind(this));
    }

    // Abuse report
    this.$el.find('.report-abuse-link').on('click', function (e) {
      e.preventDefault();
      var win = new AbuseWindow(
        this.model.get('ct'),
        this.model.get('id')
      );
    }.bind(this));

    // NGO members
    var ngo = this.model.get('ngo_list');
    if (!_.isUndefined(ngo) && ngo.count > 0) {
      $('<div class="ngo-badge-group"><div class="fa fa-bank text-green"></div></div>')
        .insertAfter(this.$('.user-avatar'));
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
    $(html).insertAfter(this.$el.find('.comment-date-from-now'));
  },

  editComment: function () {
    // We do not open the edition if it is already open!
    if (this.nowEdited !== undefined) return false;

    // We edit a non-existing comment. A template for edition and adding
    // is different!!!
    var $ed = $(_.template($('#comment-edit-template').html(), {}));
    var txt = this.model.get('comment');

    // We select a comment as currently being edited, so that we open
    // only one edition window
    this.nowEdited = true;

    // We substitue the comment with an editor
    this.$el.find('.comment-content:first').empty().append($ed);
    // We fill in the editor with the old comment
    $ed.find('#comment').val(this.model.get('comment'));

    // Save the new version of the comment
    $ed.find('.btn-submit-comment').on('click', function (e) {
      e.preventDefault();
      this.model.url = '/rest/comments/' + this.model.get('id') + '/';
      this.model.save({
        comment: $ed.find('#comment').val(),
        submit_date: moment().format()
      }, { patch: true }); // update through PATCH
      // Delete the editor and show an updated comment.
      $ed.empty().remove();
      delete this.nowEdited;
      this.$el.find('.comment-content:first')
      .text(this.model.get('comment'));
    }.bind(this));

    // Cancel action - edition cancellation
    $ed.find('.btn-cancel-comment').on('click', function (e) {
      e.preventDefault();
      $ed.empty().remove();
      delete this.nowEdited;
      this.$el.find('.comment-content:first').text(txt);
    }.bind(this));
  },

  renderReplies: function () {
    // Displays a list of answers by creation of views for each answer
    // in collection.
    this.collection.each(function (item) {
      // We define the list so that we don't add answers to answers
      var $list = this.$el.find('.subcomments:first');
      var comment = new CommentView({ model:item });
      comment.parentView = this.parentView;
      // We add comments to a ready list
      $(comment.render().el).appendTo($list);
    }, this);
  },

  replyComment: function () {
    // Same as during edition, we make sure that only one window is open
    if (this.parentView.nowAnswered !== undefined) {
      if (this.parentView.nowAnswered === this) return false;
      this.parentView.nowAnswered.$el.
      find('form, .comment-avatar-col').empty().remove();
    }
    // We tag a comment as "open" to answer.
    this.parentView.nowAnswered = this;

    // An answer to a comment. This function can definitely look better.
    var $form = $(_.template($('#comment-form-template').html(), {}));
    // We must be sure that we add elements to the parent and not
    // to some answers
    var $list = $(this.$el.find('.subcomments:first'));
    // Show the form after clicking on the link
    $form.insertBefore($list);
    // Form submit - we create an authentic comment
    $form.on('submit', function (e) {
      e.preventDefault();
      var model = new CommentModel({
        comment: $form.find('textarea').val(),
        parent: this.model.get('id'),
        ngo_list: CivilApp.user.organizations
      });
      // We do not allow empty comments
      if (model.get('comment').length <= 0) {
        alert(gettext("Comment cannot be empty"));
        return false;
      }
      // FIXME: we assign the url model by hand due to problems
      // with controlling inner events in elements. It is worth looking
      // for a better solution and to delegate those taks to the collection.
      model.url = '/rest/comments/';
      var comment = new CommentView({
        model: model
      });
      this.collection.add(model);
      model.save();
      $form.empty().remove();
      // Another filthy element - this should be evoked after
      // the adding a new element to the collection
      $(comment.render().el).appendTo($list);
      delete this.parentView.nowAnswered;
    }.bind(this));
    // Action ancellation Anulowanie - we close the edition window
    $form.find('.btn-cancel-comment').on('click', function (e) {
      e.preventDefault();
      $form.empty().remove();
      delete this.parentView.nowAnswered;
    }.bind(this));
  },

  toggleReplies: function () {
    // Show/hide answers to this comment
    var $toggle = this.$el.find('.show-replies');
    var $sublist = this.$el.find('.subcomments');

    if ($sublist.is(':visible')) {
      $sublist.slideUp('fast', function () {
        $toggle.text(gettext('(show)'));
      });
    } else {
      $sublist.slideDown('fast', function () {
        $toggle.text(gettext('(hide)'));
      });
    }
  },

  _sendVote: function (vote, vStart) {
    var self = this;
    var vTotal = this.model.get('total_votes');
    var totalVotes = vote == 'up' ? ++vTotal : --vTotal;
    var votes = ++vStart;

    $.ajax({
      type: 'POST',
      url: '/rest/votes/',
      data: {
        vote: vote,
        comment: self.model.get('id')
      },
      // Response returns an error only in the case of server error,
      // also in 'resp' object we wend additional information 'success'
      // (true or false) and we display an alert.
      success: function (resp) {
        if (resp.success === true) {
          self.model.set('upvotes', votes);
          self.model.set('total_votes', totalVotes);
          // FIXME: transfer this to one function
          self.render();
          self.renderReplies();
          message.success(resp.message);
        } else {
          message.alert(resp.message);
        }
      },
      error: function (err) {
        console.log(err);
      }
    });
  },

  voteUp: function () {
    this._sendVote('up', this.model.get('upvotes'));
  },

  voteDown: function () {
    this._sendVote('down', this.model.get('downvotes'));
  }
});

return CommentView;

});
