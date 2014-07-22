//
// ideaView.js
// ===========
// Single list entry view.
define(['jquery',
        'underscore',
        'backbone',
        'js/ideas/votes/counterWindow',
        'bootstrap',
        'moment'],

function ($, _, Backbone, CounterWindow) {
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
            this.$el.find('.date-created')
                .text(moment(this.model.get('date_created')).fromNow());
            if (this.model.get('edited')) {
                this.$el.find('.date-edited')
                    .text(moment(this.model.get('date_edited')).fromNow());
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

        voteCounterWindow: function () {
            // Extend counter window to pass model ID.
            var CW = CounterWindow.extend({
                'ideaId': this.model.get('id')
            });
            var cc = new CW();
        }
    });
    
    return IdeaView;
});