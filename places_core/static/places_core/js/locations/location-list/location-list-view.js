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
            var newTitle = gettext("Stop following");
            $.post('/add_follower/' + targetID + '/', 
                {csrfmiddlewaretoken: getCookie('csrftoken')}, 
            function (resp) {
                $(e.currentTarget)
                    .addClass('unfollow-entry fa-eye-slash')
                    .removeClass('follow-entry fa-eye');
            });
        },
        
        unfollow: function (e) {
            e.preventDefault();
            var targetID = $(e.currentTarget).attr('data-target');
            var newTitle = gettext("Follow");
            $.post('/remove_follower/' + targetID + '/', 
                {csrfmiddlewaretoken: getCookie('csrftoken')}, 
                function (resp) {
                $(e.currentTarget)
                    .addClass('follow-entry fa-eye')
                    .removeClass('unfollow-entry fa-eye-slash');
            });
        }
    });
    
    return LocationListView;
});