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

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                return this;
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
                console.log(that.collection.url);
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
