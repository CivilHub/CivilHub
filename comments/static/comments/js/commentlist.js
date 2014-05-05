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
        commentlist = commentlist || {},
        setCurrentDate = function (date) {
            var years   = date.getFullYear(),
                months  = (date.getMonth() + 1).pad(2),
                days    = date.getDate().pad(2),
                hours   = date.getHours(),
                minutes = date.getMinutes();
                return [years, '-', months, '-', days, 'T',
                        hours, ':', minutes, 'Z'].join('');
        };
    //
    // Comment model
    // -------------------------------------------------------------------------
    commentlist.Comment = Backbone.Model.extend({
        defaults: {
            comment: 'Lorem ipsum',
            content_id: $('#target-id').val(),
            content_type: $('#target-type').val(),
            username: $('#target-user').val(),
            avatar: $('#target-avatar').val(),
            replies: 0
        }
    });
    //
    // Comment view
    // -------------------------------------------------------------------------
    commentlist.CommentView = Backbone.View.extend({
        tagName: 'div',
        className: 'comment well',
        template: _.template($('#comment-template').html()),
        
        sublist: {}, // Placeholder for comment replies.
        
        counter: {}, // Placeholder for reply counter.
        
        events: {
            'click .show-replies': 'showReplies',
            'click .comment-reply': 'replyComment'
        },
        
        render: function () {
            var _that = this;
            _that.$el.html(_that.template($.extend(_that.model.toJSON())));
            _that.counter = _that.$el.find('.reply-counter');
            if (_that.model.get('replies') > 0) {
                $.get('/rest/comments/' + _that.model.id + '/replies/', function (replies) {
                    _that.sublist = 
                        new commentlist.SublistView(replies, 
                            _that.$el.find('.subcomments'));
                });
            }
            return _that;
        },
        
        showReplies: function () {
            var $a = this.$el.find('.subcomments');
            if ($a.is(':visible')) {
                $a.css('display', 'none');
            } else {
                this.$el.find('.subcomments').css('display', 'block');
            }
            return false;
        },
        
        replyComment: function () {
            var _that = this, comment = {},
                $form = $(_.template($('#comment-form-template').html(), {}));
            if (_that.$el.find('form').length > 0) {
                return false;
            }
            $form.insertAfter(_that.$el.find('p:last')).find('textarea').focus();
            //~ $('.comment-form-body').find('textarea').on('focusout', function () {
                //~ $form.empty().remove();
            //~ });
            $form.on('submit', function (evt) {
                evt.preventDefault();
                if (_.isEmpty(_that.sublist)) {
                    _that.sublist = 
                        new commentlist.SublistView([], 
                            _that.$el.find('.subcomments'));
                }
                comment = $form.find('#comment').val();
                _that.sublist.addComment(comment, _that.model.get('id'));
                _that.counter.text(parseInt(_that.counter.text(), 10) +1);
                $form.empty().remove();
                return false;
            });
            return false;
        }
    });
    //
    // Comment replies
    // -------------------------------------------------------------------------
    commentlist.SublistView = Backbone.View.extend({
        el: null,
        
        initialize: function (initialComments, bodyElement) {
            this.el = bodyElement;
            this.$el = $(bodyElement);
            this.collection = new commentlist.Commentlist(initialComments);
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
                    submit_date: setCurrentDate(new Date()),
                    parent: parentId
                }
                comment = new commentlist.Comment(formData);
            comment.url = '/rest/comments/';
            _that.collection.add(comment);
            $.ajaxSetup({
                headers: {'X-CSRFToken': getCookie('csrftoken')}
            });   
            comment.save();
            return false;
        },
        
        renderComment: function (item) {
            var CommentView = new commentlist.CommentView({
                model: item
            });
            $(CommentView.render().el).prependTo(this.$el);
            $('.subcomment-count').text(this.collection.length);
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
                $fTpl = $(_.template($('#comment-form-template').html(), {})),
                $comment = {};
                
            $fTpl.prependTo(_that.$el);
                
            $comment = $fTpl.find('textarea');
    
            $fTpl.on('submit', function (evt) {
                evt.preventDefault();
                formData = {
                    comment: $comment.val(),
                    submit_date: setCurrentDate(new Date())
                }
                comment = new commentlist.Comment(formData);
                comment.url = '/rest/comments/';
                _that.collection.add(comment);
                $.ajaxSetup({
                    headers: {'X-CSRFToken': getCookie('csrftoken')}
                });   
                comment.save();
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