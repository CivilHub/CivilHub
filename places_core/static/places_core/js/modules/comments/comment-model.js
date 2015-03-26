//
// comment-model.js
// ================

// A basic model for comments

define(['jquery',
				'underscore',
				'backbone',
				'moment'],

function ($, _, Backbone, moment) {
	
"use strict";

var CommentModel = Backbone.Model.extend({
	
	defaults: {
		user: 0, // This is necessary - we avoid 'Undefined error`
		comment: 'Lorem ipsum',
		content_id: $('#target-id').val(),
		content_type: $('#target-type').val(),
		username: $('#target-user').val(),
		user_full_name: $('#target-user-fullname').val(),
		avatar: $('#target-avatar').val(),
		replies: 0,
		total_votes: 0,
		upvotes: 0,
		downvotes: 0,
		submit_date: moment().format()
	},

	validate: function (attrs, options) {
		if (attrs.comment === undefined || attrs.comment.len <= 0) {
			return gettext("Comment cannot be empty");
		}
	}
});

return CommentModel;

});