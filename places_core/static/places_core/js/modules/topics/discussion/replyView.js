//
// replyView.js
// ============
// Single reply.

define(['jquery',
        'underscore',
        'backbone',
        'moment'],

function ($, _, Backbone, utils) {
    
    "use strict";
    
    var currentLang = window.CivilApp.language || 'en';
    
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
            this.$el.find('.date-created')
                .text(moment(this.model.get('date_created'))
                    .lang(currentLang).fromNow());
            if (this.model.get('edited')) {
                this.$el.find('.date-edited')
                    .text(moment(this.model.get('date_edited'))
                        .lang(currentLang).fromNow());
            }
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