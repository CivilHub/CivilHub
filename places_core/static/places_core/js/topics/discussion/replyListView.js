//
// replyListView.js
// ================
// Main application view.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/topics/discussion/replyCollection',
        'js/topics/discussion/replyView',
        'js/ui/paginatorView'],

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
            //~ $('body').on('click', function (e) {
                //~ self.collection.getNextPage({
                    //~ data: {
                        //~ pk: targetId
                    //~ }
                //~ });
            //~ });
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