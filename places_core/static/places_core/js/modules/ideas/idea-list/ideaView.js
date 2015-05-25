//
// ideaView.js
// ===========
// Single list entry view.
define(['jquery',
        'underscore',
        'backbone',
        'js/modules/ideas/votes/counterWindow',
        'bootstrap',
        'moment'],

function ($, _, Backbone, CounterWindow) {
    
    "use strict";
    
    var currentLang = window.CivilApp.language || 'en';
    
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

        openMenu: function () {
            if (this.submenu.opened) {
                this.submenu.$el.slideUp('fast');
                this.submenu.opened = false;
            } else {
                this.submenu.$el.slideDown('fast');
                this.submenu.opened = true;
            }
        },

        voteCounterWindow: function (e) {
            // Extend counter window to pass model ID.
            var CW = CounterWindow.extend({
                'ideaId': $(e.currentTarget).attr('data-target')
            });
            var cc = new CW();
        }
    });
    
    return IdeaView;
});
