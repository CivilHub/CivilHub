//
// location-list-view.js
// =====================

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/locations/follow-button'],

function ($, _, Backbone, fb) {

"use strict";

var LocationListView = Backbone.View.extend({

  tagName: 'li',

  className: 'location-list-entry',

  template: _.template($('#location-entry-tpl').html()),

  events: {
    'click .hide-details': 'hideDetails',
    'click .follow-btn': 'follow'
  },

  render: function () {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  },

  hide: function () {
    this.$el.css('display', 'none');
    return this;
  },

  show: function () {
    this.$el.css('display', 'block');
    return this;
  },

  details: function () {
    var $ol = this.$el.find('.list-entry-details');
    var $parent = this.$el.parent();

    $parent.children().hide();
    $ol.parent().show();
    $ol.css({
      position: 'absolute',
      left: $parent.parent().position().left,
      top: $parent.parent().position().top - 40,
      width: $parent.width(),
      height: $parent.height() + 20,
      zIndex: 1001
    }).fadeIn('fast');
  },

  hideDetails: function () {
    $('.is-empty-list').empty().remove();
    this.$el.parent().children().show();
    this.$el.find('.list-entry-details').fadeOut('slow');
    if (this.parentView.sublist !== undefined) {
      this.parentView.sublist.destroy();
    }
  },

  follow: function (e) {
    e.preventDefault();
    var $this = $(e.currentTarget);
    var id = $this.attr('data-target');
    fb.followRequest(id, function (response) {
      $this.text(fb.settext(response.following))
        .toggleClass('btn-follow-location btn-follow-entry')
        .toggleClass('btn-unfollow-location btn-unfollow-entry');
    }, $this);
  }

});

return LocationListView;

});
