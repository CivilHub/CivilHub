//
// replyListView.js
// ================
// Main application view.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/modules/topics/discussion/replyCollection',
        'js/modules/topics/discussion/replyView',
        'js/modules/ui/paginatorView'],

function ($, _, Backbone, ReplyCollection, ReplyView, PaginatorView) {
    "use strict";
    
    var ReplyListView = Backbone.View.extend({
        
        el: '.main-content',
        
        initialize: function () {
            var self = this,
                targetId = $('#discussion-id').val();
            this.listElement = this.$el.find('#replies');
            this.collection = new ReplyCollection();
            this.collection.fetch({
                data: {pk: targetId},
                success: function () {
                    self.paginator = new PaginatorView({
                        count: self.collection.totalResultsCounter,
                        perPage: 2,
                        targetCollection: self.collection,
                        data: {
                            pk: targetId
                        }
                    });
                    $(self.paginator.render().el).appendTo(self.$el);
                }
            });
            this.listenTo(this.collection, 'sync', this.render);
        },
        
        render: function () {
            this.listElement.empty();
            this.collection.each(function (item) {
                this.renderEntry(item);
            }, this);
        },
        
        renderEntry: function (item) {
            var reply = new ReplyView({
                model: item
            });
            $(reply.render().el).appendTo(this.listElement);
        }
    });
    
    return ReplyListView;
});