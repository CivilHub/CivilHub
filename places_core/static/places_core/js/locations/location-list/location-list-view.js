//
// location-list-view.js
// =====================

define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    var LocationListView = Backbone.View.extend({
        
        tagName: 'li',
        
        className: 'location-list-entry',
        
        template: _.template($('#location-entry-tpl').html()),
        
        events: {
            'click .follow-entry': 'follow',
            'click .unfollow-entry': 'unfollow'
        },
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        
        follow: function (e) {
            e.preventDefault();
            var targetID = $(e.currentTarget).attr('data-target');
            $.post('/add_follower/' + targetID + '/', 
                {csrfmiddlewaretoken: getCookie('csrftoken')}, 
            function (resp) {
                $(e.currentTarget)
                    .addClass('unfollow-entry')
                    .removeClass('follow-entry')
                    .text(gettext("Stop following"));
            });
        },
        
        unfollow: function (e) {
            e.preventDefault();
            var targetID = $(e.currentTarget).attr('data-target');
            $.post('/remove_follower/' + targetID + '/', 
                {csrfmiddlewaretoken: getCookie('csrftoken')}, 
                function (resp) {
                $(e.currentTarget)
                    .addClass('follow-entry')
                    .removeClass('unfollow-entry')
                    .text(gettext("Follow"));
            });
        }
    });
    
    return LocationListView;
});