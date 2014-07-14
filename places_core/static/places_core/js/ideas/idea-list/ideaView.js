//
// ideaView.js
// ===========
// Single list entry view.
define(['jquery',
        'underscore',
        'backbone',
        'bootstrap'],

function ($, _, Backbone) {
    "use strict";
    
    var IdeaView = Backbone.View.extend({
        tagName: 'div',

        className: 'row idea-entry',

        template: _.template($('#idea-entry-tpl').html()),

        submenu: {},

        events: {
            'click .submenu-toggle': 'openMenu',
            'click .idea-vote-count': 'voteCounterWindow'
        },

        render: function () {
            var that = this;
            this.$el.html(this.template(this.model.toJSON()));
            this.submenu = {
                $el: that.$el.find('.entry-submenu'),
                opened: false
            };
            this.$el.find('.vote-btn').tooltip({
                placement: 'right'
            });
            return this;
        },

        openMenu: function () {
            if (this.submenu.opened) {
                this.submenu.$el.slideUp('fast');
                this.submenu.opened = false;
            } else {
                this.submenu.$el.slideDown('fast');
                this.submenu.opened = true;
            }
        },

        voteCounterWindow: function () {
            //var cc = CivilApp.voteCounter(this.model.get('id'));
        }
    });
    
    return IdeaView;
});