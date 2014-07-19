//
// replyListView.js
// ================
// Main application view.
//
define(['jquery',
        'underscore',
        'backbone',
        'js/topics/discussion/replyCollection',
        'js/topics/discussion/replyView'],

function ($, _, Backbone, ReplyCollection, ReplyView) {
    "use strict";
    
    var ReplyListView = Backbone.View.extend({
        
        el: '#replies',
        
        initialize: function () {
            var self = this;
            this.collection = new ReplyCollection();
            this.collection.targetId = $('#discussion-id').val();
            this.collection.currentPage = 1;
            this.collection.fetch({
                data: {pk: $('#discussion-id').val()}
            });
            this.listenTo(this.collection, 'sync', this.render);
            
            $('body').on('click', function (e) {
                self.collection.getPage();
            });
        },
        
        render: function () {
            this.$el.empty();
            this.collection.each(function (item) {
                this.renderEntry(item);
            }, this);
        },
        
        renderEntry: function (item) {
            var reply = new ReplyView({
                model: item
            });
            $(reply.render().el).appendTo(this.$el);
        }
    });
    
    return ReplyListView;
});