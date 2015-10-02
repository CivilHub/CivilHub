/**
 * detail.js
 * =========
 *
 * Simplified view to manage righ sidebar with detail information.
 * This view uses the same model as the main application.
 */

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/inlines/list',
        'text!js/modules/mapvotes/common/templates/detail.html',
        'text!js/modules/mapvotes/common/templates/postbox.html',
        'bootbox'],

function ($, _, Backbone, CommentListView, html, postboxHtml) {

"use strict";

var HTML = VA__MAP_DATA.enabled ? html + postboxHtml : html;

var DetailView = Backbone.View.extend({

  template: _.template(HTML),

  events: {
    'click .vote-btn': 'vote'
  },

  render: function () {
    this.cleanup();
    this.$el.html(this.template(this.model.toJSON()));

    // Create and adjust vote button
    this.voteButton();

    // Display people that already voted for this marker
    _.each(this.model.get('voters'), function (voter) {
      var $el = $('<img src="' + voter.profile.thumbnail + '">');
      $el.appendTo(this.$el.find('.voters'));
    }, this);

    // Initialize inline comment application
    this.enableComments();

    this.listenTo(this.model, 'change:user_vote', this.voteButton);
    this.listenTo(this.model, 'voteError', this.voteError);

    return this;
  },

  voteButton: function () {
    if (!VA__MAP_DATA.enabled) {
      return;
    }

    if (this.model.get('user_vote')) {
      this.$('.vote-btn')
        .removeClass('btn-success')
        .addClass('btn-danger')
        .text(gettext("Revoke vote"));
    } else {
      this.$('.vote-btn')
        .removeClass('btn-danger')
        .addClass('btn-success')
        .text(gettext("Vote YES"));
    }
  },

  enableComments: function () {
    this.comments = new CommentListView({
      $el: this.$('.commentarea'),
      url: '/api-comments/list/',
      ct: this.model.get('content_type'),
      pk: this.model.get('id'),
      page: 1,
      data: this.model.get('comment_meta')
    });
    this.listenTo(this.comments, 'commentadd', function (comment) {
      var meta = _.clone(this.model.get('comment_meta'));
      meta.results.unshift(comment);
      this.model.set('comment_meta', meta);
    });
  },

  cleanup: function () {
    this.stopListening(this.comments, 'commentadd');
    this.stopListening(this.model);
    this.comments = null;
  },

  vote: function (e) {
    this.model.vote();
  },

  voteError: function (err) {
    bootbox.alert(err);
  }
});

return DetailView;

});

