//
// comment-model.js
// ================
// Podstawowy model dla komentarza.

define(['jquery',
        'underscore',
        'backbone',
        'moment'],

function ($, _, Backbone, moment) {
    
    "use strict";
    
    var CommentModel = Backbone.Model.extend({
        
        defaults: {
            user: 0, // Konieczne - unikamy `Undefined error`
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
        }
    });
    
    return CommentModel;
});