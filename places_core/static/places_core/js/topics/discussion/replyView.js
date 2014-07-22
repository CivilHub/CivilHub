//
// replyView.js
// ============
// Single reply.
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone, utils) {
    "use strict";
    
    var getCookie = function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    
    var ReplyView = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'reply-entry',
        
        template: _.template($('#reply-tpl').html()),
        
        render: function () {
            var self = this;
            this.$el.html(this.template(this.model.toJSON()));
            this.$el.find('.entry-vote-up').on('click', function (e) {
                e.preventDefault();
                self.sendVote(true);
            });
            this.$el.find('.entry-vote-down').on('click', function (e) {
                e.preventDefault();
                self.sendVote(false);
            });
            return this;
        },
        
        sendVote: function (vote) {
            var self = this;
            $.ajax({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                },
                type: 'POST',
                url: '/discussion/' + this.model.get('id') + '/vote/',
                data: {vote: vote},
                success: function (resp) {
                    resp = JSON.parse(resp);
                    console.log(resp);
                    if (resp.success) {
                        var votes = parseInt(self.model.get('vote_count'), 10);
                        self.$el.find('.entry-vote-count').text(++votes);    
                    }
                },
                error: function (err) {
                    console.log(err);
                }
            });
        }
    });
    
    return ReplyView;
});