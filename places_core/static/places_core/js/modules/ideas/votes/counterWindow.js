//
// counterWindow.js
// ================

// Modal window with idea votes summary.

define(['jquery',
				'underscore',
				'backbone',
				'js/modules/ideas/votes/voteCollection',
				'js/modules/ideas/votes/voteView',
				'bootstrap'],

function ($, _, Backbone, VoteCollection, VoteView) {

	"use strict";
	
	var CounterWindow = Backbone.View.extend({
		
		el: '#vote-counter-modal',
		
		initialize: function (options) {
			
			var that = this,
				positive_votes = [],
				negative_votes = [],
				data = {};
				
			if (options.ideaId) {
				this.ideaId = options.ideaId;
			} 
			if (this.ideaId) data = {pk: this.ideaId};
			
			$.ajax({
				type: 'GET',
				url: '/rest/idea_votes/',
				data: data,
				success: function (votes) {
					_.each(votes, function (item) {
						if (item.vote) {
							positive_votes.push(item);
						} else {
							negative_votes.push(item);
						}
					});
					that.positive_collection = new VoteCollection(positive_votes);
					that.negative_collection = new VoteCollection(negative_votes);
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
			var entry = new VoteView({
				model: item
			});
			$(entry.render().el).appendTo(this.$pEntries);
		},
		
		renderNegativeEntry: function (item) {
			var entry = new VoteView({
				model: item
			});
			$(entry.render().el).appendTo(this.$nEntries);
		}
	});
	
	return CounterWindow;
});