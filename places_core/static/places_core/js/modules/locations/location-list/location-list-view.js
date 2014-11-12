//
// location-list-view.js
// =====================

define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    /*
     * Simple helper functions to detect IE and Safari browsers, wich have
     * some problems with advanced CSS rendering, so we need to adjust styles
     * later (thank you, IE).
     */
    
    function isSafari () {
        var n = window.navigator.userAgent;
        return (/Safari/).test(n);
    }
    function isIE () {
        var n = window.navigator.userAgent;
        return (/MSIE/).test(n) || (/Trident/).test(n);
    }
    
    var LocationListView = Backbone.View.extend({
        
        tagName: 'li',
        
        className: 'location-list-entry',
        
        template: _.template($('#location-entry-tpl').html()),
        
        events: {
            'click .hide-details': 'hideDetails',
            'click .follow-entry': 'follow',
            'click .unfollow-entry': 'unfollow'
        },
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        
        hide: function () {
            this.$el.css('display', 'none');
            return this;
        },
        
        show: function () {
            this.$el.css('display', 'block');
            return this;
        },
        
        details: function () {
            var $ol = this.$el.find('.list-entry-details'),
                $parent = this.$el.parent();

            $parent.children().hide();
            $ol.parent().show();
            $ol.css({
                position: 'absolute',
                left: $parent.parent().position().left,
                top: $parent.parent().position().top - 40,
                width: $parent.width(),
                height: $parent.height() + 20,
                zIndex: 1001
            }).fadeIn('fast');
        },
        
        hideDetails: function () {
            $('.is-empty-list').empty().remove();
            this.$el.parent().children().show();
            this.$el.find('.list-entry-details').fadeOut('slow');
            if (this.parentView.sublist !== undefined) {
                this.parentView.sublist.destroy();
            }
        },
        
        follow: function (e) {
            e.preventDefault();
            var targetID = $(e.currentTarget).attr('data-target');
            var newTitle = gettext("Stop following");
            $.post('/add_follower/' + targetID + '/',
                {csrfmiddlewaretoken: getCookie('csrftoken')}, 
            function (resp) {
                $(e.currentTarget)
                    .addClass('unfollow-entry btn-unfollow-location')
                    .removeClass('follow-entry btn-follow-location')
                    .text(newTitle);
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
                    .addClass('follow-entry btn-follow-location')
                    .removeClass('unfollow-entry btn-unfollow-location')
                    .text(newTitle);
            });
        }
    });
    
    return LocationListView;
});