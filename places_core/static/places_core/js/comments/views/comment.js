var app = app || {};

app.CommentView = Backbone.View.extend({
    tagName: 'div',
    className: 'comment',
    template: _.template($('#comment-template').html()),
    
    render: function () {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});