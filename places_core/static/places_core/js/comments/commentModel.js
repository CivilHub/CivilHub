//
// commentModel.js
// ===============
// Basic model for all comments.
define(['jquery',
        'backbone'],

function ($, Backbone) {
    "use strict";
    
    var CommentModel = Backbone.Model.extend({
        defaults: {
            user: 0,
            comment: 'Lorem ipsum',
            content_id: $('#target-id').val(),
            content_type: $('#target-type').val(),
            username: $('#target-user').val(),
            user_full_name: $('#target-user-fullname').val(),
            avatar: $('#target-avatar').val(),
            replies: 0,
            total_votes: 0,
            upvotes: 0,
            downvotes: 0
        }
    });
    
    return CommentModel;
});