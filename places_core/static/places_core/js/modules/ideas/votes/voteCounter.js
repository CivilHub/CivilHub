//
// voteCounter.js
// ==============

// Modal window with list of users that voted on this particular idea.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/utils/utils',
        'js/modules/ui/ui',
        'bootstrap'],

function ($, _, Backbone, utils, ui) {

  "use strict";

  Counter.VoteModel = Backbone.Model.extend({});

  Counter.VoteView = Backbone.View.extend({

    tagName:   'li',

    className: 'entry',

    template:  _.template($('#vote-counter-entry').html()),

    render: function () {
      this.$el.html(this.template(this.model.toJSON()));
      this.markLabel(this.model.get('vote'));
      return this;
    },

    markLabel: function (vote) {
      var $label = this.$el.find('.vote-result-label'),
        $labelTxt = $label.find('.fa');
      if (vote) {
        $label.addClass('label-success');
        $labelTxt.addClass('fa-arrow-up');
      } else {
        $label.addClass('label-danger');
        $labelTxt.addClass('fa-arrow-down');
      }
    }
  }),

  Counter.CountList = Backbone.Collection.extend({
    model: Counter.VoteModel
  }),

  Counter.Window = Backbone.View.extend({

    el: '#vote-counter-modal',

    initialize: function () {

      var that = this,
        positive_votes = [],
        negative_votes = [];

      $.ajax({
        type: 'GET',
        url: '/rest/idea_votes/',
        data: {pk: that.model.get('id')},
        success: function (votes) {
          console.log(votes);
          _.each(votes, function (item) {
            console.log(item);
            if (item.vote) {
              positive_votes.push(item);
            } else {
              negative_votes.push(item);
            }
          });
          that.positive_collection = new Counter.CountList(positive_votes);
          that.negative_collection = new Counter.CountList(negative_votes);
          that.$pEntries = that.$el.find('.positive-votes');
          that.$pCounter = that.$el.find('.positive-counter');
          that.$pEntries.empty();
          that.$nEntries = that.$el.find('.negative-votes');
          that.$nCounter = that.$el.find('.negative-counter');
          that.$nEntries.empty();
          that.render();
        }
      });
    },

    render: function () {
      this.positive_collection.each(function (item) {
        this.renderPositiveEntry(item);
      }, this);
      this.$pCounter.text(this.positive_collection.length);
      this.negative_collection.each(function (item) {
        this.renderNegativeEntry(item);
      }, this);
      this.$nCounter.text(this.negative_collection.length);
      this.$el.modal('show').data('voteCounter', this);
    },

    renderPositiveEntry: function (item) {
      var entry = new Counter.VoteView({
        model: item
      });
      $(entry.render().el).appendTo(this.$pEntries);
    },

    renderNegativeEntry: function (item) {
      var entry = new Counter.VoteView({
        model: item
      });
      $(entry.render().el).appendTo(this.$nEntries);
    }
  });

  return Counter;
});