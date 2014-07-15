//
// commentListView.js
// ==================
// First-level comment list view.
define(['jquery',
        'underscore',
        'backbone',
        'moment',
        'js/comments/commentModel',
        'js/comments/commentCollection',
        'js/comments/commentView'],

function ($, _, Backbone, moment, CommentModel, CommentCollection, CommentView) {
    "use strict";
    console.log("CommentView");
    console.log(CommentView);
    // Set apps url
    var commentlist = commentlist || {},
        
        incrementCommentCounter = function () {
            var $counter = $('.comment-count'),
                value = parseInt($counter.text(), 10),
                nVal = 1;
            if (!_.isNaN(value)) {
                nVal = ++value;
            }
            $counter.text(nVal);
        },
        
        CommentListView = Backbone.View.extend({
            el: '#comments',
            
            addComment: function () {
                var _that = this,
                    formData = {},
                    comment = {},
                    $fTpl = $('#user-comment-form'),
                    $comment = {};
                    
                $comment = $fTpl.find('textarea');
                
                formData = {
                    comment: $comment.val(),
                    submit_date: moment().format()
                };
                comment = new CommentModel(formData);
                comment.url = '/rest/comments/';
                _that.collection.add(comment);
                $.ajaxSetup({
                    headers: {'X-CSRFToken': getCookie('csrftoken')}
                });   
                comment.save();
                incrementCommentCounter();
                $comment.val('');
            },
            
            initialize: function () {
                var _that = this;
                _that.render();
                _that.listenTo(_that.collection, 'add', _that.renderComment);
                _that.listenTo(_that.collection, 'reset', _that.reRender);
                $('.btn-submit-comment-main').on('click', function (evt) {
                    evt.preventDefault();
                    _that.addComment(); 
                });
                // Reorder comments by submit date or by vote number
                $('.change-order-link').on('click', function (evt) {
                    evt.preventDefault();
                    $('.comment').empty().remove();
                    _that.collection.fetch({
                        url: url + '&order=' + $(this).attr('data-order'),
                        reset:true
                    });
                    return false;
                });
            },
            
            render: function () {
                this.collection.each(function (item) {
                    this.renderComment(item);
                }, this);
            },
            
            reRender: function () {
                var startPosition = $('.change-order-link:first').position().top;
                this.render();
                $(window).scrollTop(startPosition - 85);
            },
            
            renderComment: function (item) {
                var comment = new CommentView({
                    model: item
                });
                $(comment.render().el)
                    .insertAfter(this.$el.find('.commentformarea'));
            }
        });
    
    return CommentListView;
});