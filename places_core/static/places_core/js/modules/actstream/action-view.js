//
// actionView.js
// =============

// Single action entry view.

define(['underscore',
        'backbone',
        'moment',
        'js/modules/utils/utils',
        'text!js/modules/actstream/templates/simple-action.html',
        'text!js/modules/actstream/templates/content-action.html'],

function (_, Backbone, moment, utils, html, contentHtml) {

"use strict";

var FIXED_ITEMS = ['idea', 'discussion', 'news', 'poll', 'locationgalleryitem'];

var ActionView = Backbone.View.extend({

  id: 'tour-activity',

  tagName: 'li',

  className: 'timeline-item',

  template: _.template(html),

  contentTemplate: _.template(contentHtml),

  render: function () {
    var attrs = this.model.toJSON();
    var tpl = this.template;
    if (!_.isNull(attrs.action_object) &&
      _.indexOf(FIXED_ITEMS, attrs.action_object.content_type.type) >= 0) {
      tpl = this.contentTemplate;
    }
    attrs.timestamp = moment(attrs.timestamp).fromNow();
    this.$el.html(tpl(attrs));
    this.$('.date').tooltip();
    this.fixImage();
    return this;
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
      $image.insertAfter(this.$('.full-click-box:first')).attr('src', src);
    }
  }
});

return ActionView;

});
