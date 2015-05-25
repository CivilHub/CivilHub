//
// actionView.js
// =============

// Single action entry view.

define(['jquery',
        'underscore',
        'backbone',
        'moment',
        'js/modules/utils/utils',
        'js/modules/inlines/list',
        'text!js/modules/actstream/templates/simple-action.html',
        'text!js/modules/actstream/templates/content-action.html',
        'text!js/modules/actstream/templates/comment-action.html'],

function ($, _, Backbone, moment, utils, CommentListView, html, contentHtml, commentHtml) {

"use strict";

$.fn.commentList = function (options) {
  var defaults = {
    url: '/api-comments/list/',
    currentPage: 1
  };
  options = _.extend(defaults, options);
  return $(this).each(function () {
    var $this = $(this);
    options = _.extend(options, {
      $el: $this,
      ct: $this.attr('data-ct'),
      pk: $this.attr('data-pk'),
      count: $this.attr('data-count')
    });
    var commentlist = new CommentListView(options);
    $this.data('commentlist', commentlist);
    return this;
  });
};

var FIXED_ITEMS = [
  'idea',
  'discussion',
  'news',
  'poll',
  'locationgalleryitem',
  'blogentry'
];

var COMMENTED_ITEMS = ['vote', 'commentvote'];

var ActionView = Backbone.View.extend({

  id: 'tour-activity',

  tagName: 'li',

  className: 'timeline-item',

  template: _.template(html),

  contentTemplate: _.template(contentHtml),

  commentTemplate: _.template(commentHtml),

  events: {
    'click .comment-toggle': 'toggleComments',
    'click .show-more': 'fetchComments'
  },

  initialized: false,

  render: function () {
    var attrs = this.model.toJSON();
    var tpl = this.selectTemplate();
    _.bindAll(this, 'toggleComments');
    _.bindAll(this, 'fetchComments');
    attrs.timestamp = moment(attrs.timestamp).fromNow();
    this.$el.html(tpl(attrs));
    this.$('.date').tooltip();
    this.fixImage();
    this.applyComments();
    return this;
  },

  selectTemplate: function () {
    var attrs = this.model.toJSON();
    var tpl = this.template;
    var ct;
    if (!_.isNull(attrs.action_object)) {
      ct = attrs.action_object.content_type.type;
      if (_.indexOf(FIXED_ITEMS, ct) !== -1) {
        tpl = this.contentTemplate;
      } else if (_.indexOf(COMMENTED_ITEMS, ct) !== -1) {
        tpl = this.commentTemplate;
      }
    }
    return tpl;
  },

  fixImage: function () {
    var obj = this.model.get('action_object');
    if (_.isNull(obj)) {
      return;
    }
    var image = obj.image;
    if (_.isNull(image)) {
      return;
    }
    if (!_.isUndefined(image.thumbnail) && !image.is_default) {
      var $image = $('<img class="timeline-image">');
      var src = image.thumbnail;
      if (utils.isRetina() && !_.isUndefined(image.retina_thumbnail)) {
        src = image.retina_thumbnail;
      }
      $image.attr('src', src)
        .insertAfter(this.$('.full-click-box:first'));
    }
  },

  applyComments: function () {
    var obj = this.model.get('action_object');
    var $c = this.$('.comment-count');
    if (_.isNull(obj)) {
      return;
    }
    this.$('.comment-area')
      .commentList({ $counter: $c });
    this.comments = this.$('.comment-area')
      .data('commentlist');
  },

  toggleComments: function (e) {
    e.preventDefault();
    if (this.initialized) {
      this.$('.comment-area').toggle();
      return;
    }
    this.comments.fetch();
    this.$('.comment-area').show();
    this.initialized = true;
  },

  fetchComments: function (e) {
    e.preventDefault();
    this.comments.nextPage();
  }
});

return ActionView;

});
