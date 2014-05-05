(function ($) {
    "use strict";
    // Set apps url
    var cType = $('#target-type').val(),
        cId = $('#target-id').val(),
        cPrefix = $('#target-label').val(),
        url = ['/rest/comments?content-label=',
               cPrefix,
               '&content-type=',
               cType,
               '&content-id=',
               cId].join(''),
        commentlist = commentlist || {};
    //
    // Comment model
    // -------------------------------------------------------------------------
    commentlist.Comment = Backbone.Model.extend({
        defaults: {
            comment: 'Lorem ipsum',
            content_id: $('#target-id').val(),
            content_type: $('#target-type').val(),
            username: $('#target-user').val()
        }
    });
    //
    // Comment view
    // -------------------------------------------------------------------------
    commentlist.CommentView = Backbone.View.extend({
        tagName: 'div',
        className: 'comment well',
        template: _.template($('#comment-template').html()),
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    //
    // List all comments view
    // -------------------------------------------------------------------------
    commentlist.CommentlistView = Backbone.View.extend({
        el: '#comments',
        
        events: {
            'click .add-comment': 'addComment'
        },
        
        addComment: function () {
            var _that = this,
                formData = {},
                comment = {},
                $fTpl = $('<form></form>'),
                $comment = {},
                date = new Date(),
                years = date.getFullYear(),
                months = (date.getMonth() + 1).pad(2),
                days = date.getDate().pad(2),
                hours = date.getHours(),
                minutes = date.getMinutes(),
                currentDate = [years, '-', months, '-', days, 
                               'T', hours, ':', minutes, 'Z'];
                
            $fTpl.html($('#comment-form-template').html())
                .attr({
                    role: 'presentation',
                    id: 'comment-form-body'
                })
                .prependTo(_that.$el);
                
            $comment = $fTpl.find('textarea');
    
            $fTpl.find('form').on('submit', function (evt) {
                evt.preventDefault();
                formData = {
                    comment: $comment.val(),
                    submit_date: currentDate.join('')
                }
                comment = new commentlist.Comment(formData);
                comment.url = '/rest/comments/';
                _that.collection.add(comment);
                $.ajaxSetup({
                    headers: {'X-CSRFToken': getCookie('csrftoken')}
                });   
                comment.save();
                console.log(formData);
                console.log(comment);
                $fTpl.empty().remove();
            });
        },
        
        initialize: function (initialComments) {
            this.collection = new commentlist.Commentlist(initialComments);
            this.render();
            this.listenTo(this.collection, 'add', this.renderComment);
        },
        
        render: function () {
            this.collection.each(function (item) {
                this.renderComment(item);
            }, this);
        },
        
        renderComment: function (item) {
            var CommentView = new commentlist.CommentView({
                model: item
            });
            $(CommentView.render().el).insertAfter(this.$el);
            $('.comment-count').text(this.collection.length);
        }
    });
    //
    // Entire comments collection for selected element.
    // -------------------------------------------------------------------------
    commentlist.Commentlist = Backbone.Collection.extend({
        model: commentlist.Comment
    });
    //
    // Start Application.
    // -------------------------------------------------------------------------
    $.get(url, function (comments) {
        new commentlist.CommentlistView(comments);
    });
})(jQuery);