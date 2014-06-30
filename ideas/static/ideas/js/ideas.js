//
// Handle ideas list for single location.
// ======================================
//
(function ($) {
"use strict";

var url = window.IDEA_API_URL;

var ideaList = function () {

    var IdeaModel = Backbone.Model.extend({}),

        IdeaView = Backbone.View.extend({
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
                var cc = civApp.voteCounter(this.model.get('id'));
            }
        }),

        IdeaCollection = Backbone.Collection.extend({
            model: IdeaModel,
            url: url
        }),

        IdeasList = Backbone.View.extend({
            el: '#idea-list-view',

            initialize: function () {
                var that = this;
                that.collection = new IdeaCollection();
                that.collection.fetch({
                    success: function () {
                        that.render();
                    }
                });
            },

            render: function () {
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
            },

            renderEntry: function (item) {
                var itemView = new IdeaView({
                        model: item
                    });
                $(itemView.render().el).appendTo(this.$el);
            }
        });

    return new IdeasList();
};

var ideas = ideaList();

})(jQuery);
