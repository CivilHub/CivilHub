//
// voteView.js
// ===========

// Single entry in votes summary window.

define(['jquery',
			  'underscore',
				'backbone'],

function ($, _, Backbone) {
	
	"use strict";
	
	var VoteView = Backbone.View.extend({
			
		tagName:   'li',
		
		className: 'entry',
		
		template:  _.template($('#vote-counter-entry').html()),
		
		render: function () {
			this.$el.html(this.template(this.model.toJSON()));
			this.markLabel(this.model.get('vote'));
			this.$('.counter-entry').find('a').tooltip();
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
	});
	
	return VoteView;
});