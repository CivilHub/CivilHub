//
// subcommentView.js
// =================
// List comments that are childrens of other comments.
define(['jquery',
        'underscore',
        'backbone',
        'moment',
        'js/comments/commentModel',
        'js/comments/commentCollection',
        'js/comments/commentView'],

function ($, _, Backbone, moment, CommentModel, CommentCollection, CommentView) {
    "use strict";
    
    var SubcommentView = Backbone.View.extend({
        el: null,
        
        initialize: function (initialComments, bodyElement) {
            this.el = bodyElement;
            this.$el = $(bodyElement);
            this.collection = new CommentCollection(initialComments);
            this.render();
            this.listenTo(this.collection, 'add', this.renderComment);
        },
        
        render: function () {
            this.collection.each(function (item) {
                this.renderComment(item);
            }, this);
        },
        
        addComment: function (comment, parentId) {
            var _that = this,
                formData = {
                    comment: comment,
                    submit_date: moment().format(),
                    parent: parentId
                };
                comment = new CommentModel(formData);
            comment.url = '/rest/comments/';
            _that.collection.add(comment);
            $.ajaxSetup({
                headers: {'X-CSRFToken': getCookie('csrftoken')}
            });   
            comment.save();
            incrementCommentCounter();
            return false;
        },
        
        renderComment: function (item) {
            console.log(CommentView);
            var comment = new CommentView({
                model: item
            });
            $(comment.render().el).prependTo(this.$el);
        }
    });
    
    return SubcommentView;
});