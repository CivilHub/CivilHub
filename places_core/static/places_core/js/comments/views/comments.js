var app = app || {}

app.CommentListView = Backbone.View.extend({
    el: '.comments',
    
    initilize: function (initialComments) {
        this.collection = new app.CommentList(initialComments);
        this.render();
    },
    
    render: function () {
        this.collection.each(function (comment) {
            this.renderComment(comment);
        });
    },
    
    renderComment: function (comment) {
        var commentView = new app.CommentView({
            model: comment
        });
        this.$el.append(commentView.render().el);
    }
});
