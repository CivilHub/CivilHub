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
    incrementCommentCounter = function () {
        var $counter = $('.comment-count'),
            value = parseInt($counter.text(), 10),
            nVal = 1;
        if (!_.isNaN(value)) {
            nVal = ++value;
        }
        $counter.text(nVal);
    };
$('.comment-toggle').on('click', function () {
    if ($('#comments').is(':visible')) {
        $('#comments').slideUp('fast');
        $(this).text(gettext('Show comments'));
    } else {
        $('#comments').slideDown('fast');
        $(this).text(gettext('Hide comments'));
    }
});
//
// Comment model
// -------------------------------------------------------------------------
commentlist.Comment = Backbone.Model.extend({
    defaults: {
        comment: 'Lorem ipsum',
        content_id: $('#target-id').val(),
        content_type: $('#target-type').val(),
        username: $('#target-user').val(),
        user_full_name: $('#target-user-fullname').val(),
        avatar: $('#target-avatar').val(),
        replies: 0,
        total_votes: 0,
        upvotes: 0,
        downvotes: 0
    }
});
//
// Comment view
// -------------------------------------------------------------------------
commentlist.CommentView = Backbone.View.extend({
    tagName: 'div',
    className: 'comment',
    template: _.template($('#comment-template').html()),
    
    sublist: {}, // Placeholder for comment replies.
    
    counter: {}, // Placeholder for reply counter.
    
    sublistState: 'shown', // Track if replies are visible or not.
    
    voteCounter: {}, // Placeholder for displaying calculated votes
    
    events: {
        'click .show-replies': 'showReplies',
        'click .comment-reply': 'replyComment',
        'click .vote-up-link': 'voteUp',
        'click .vote-down-link': 'voteDown',
        'mouseover': 'showControls',
        'mouseout': 'hideControls'
    },
    
    render: function () {
        var _that = this,
            $elem = {};
        _that.$el.html(_that.template($.extend(_that.model.toJSON())));
        $elem = _that.$el.find('.comment-votes-detail:first');
        _that.counter = _that.$el.find('.reply-counter:first');
        _that.voteCounter = _that.$el.find('.comment-total-votes:first');
        if (_that.model.get('replies') > 0) {
            $.get('/rest/comments/' + _that.model.id + '/replies/', function (replies) {
                _that.sublist = 
                    new commentlist.SublistView(replies, 
                        _that.$el.find('.subcomments'));
            });
        }
        _that.$el.find('.report-abuse-link').tooltip();
        _that.voteCounter.bind('mouseenter', function (evt) {
            $elem.stop(true).fadeIn('slow');
        });
        _that.voteCounter.bind('mouseout', function (evt) {
            $elem.stop(true).fadeOut('slow');
        });
        _that.$el.find('.comment-edit:first').on('click', function (evt) {
            evt.preventDefault();
            _that.edit();
        });
        return _that;
    },
    
    showControls: function (e) {
        this.$el.find('.comment-controls:first').css('opacity', 1);
    },
    
    hideControls: function (e) {
        this.$el.find('.comment-controls:first').css('opacity', 0);
    },
    
    update: function (attrs, callback, params) {
        sendAjaxRequest('PUT', '/rest/comments/' + this.model.get('id'), {
            data: attrs,
            success: function (resp) {
                display_alert(gettext('Comment saved'));
                if (typeof(callback) === 'function') {
                    params = params || {};
                    callback(params);
                }
            },
            error: function (err) {
                console.log(err);
            }
        });
    },
    
    edit: function () {
        var _that = this,
            $content = _that.$el.find('.comment-content:first'),
            content = $content.html(),
            $editor = $('<textarea></textarea>'),
            $cancel = $('<button></button>'),
            $submit = $('<button></button>');
        $content.empty();
        $editor
            .text(content)
            .appendTo($content)
            .addClass('form-control');
        $cancel
            .insertAfter($content)
            .addClass('btn btn-default btn-sm')
            .text(gettext('Cancel'))
            .on('click', function (evt) {
                evt.preventDefault();
                _that.render();
            });
        $submit
            .insertAfter($cancel)
            .addClass('btn btn-primary btn-sm')
            .text(gettext('Save'))
            .on('click', function (evt) {
                var newContent = $editor.val();
                evt.preventDefault();
                _that.model.set('comment', newContent);
                _that.update(_that.model.toJSON(), function () {
                    _that.render();
                });
            });
    },
    
    showReplies: function () {
        var _that = this,
            $a = this.$el.find('.subcomments:first'),
            $b = this.$el.find('.show-replies:first');
        if (_that.sublistState === 'shown') {
            $a.slideUp('fast');
            $b.text(gettext('(show)'));
            _that.sublistState = 'hidden';
        } else {
            $a.slideDown('fast');
            $b.text(gettext('(hide)'));
            _that.sublistState = 'shown';
        }
        return false;
    },
    
    replyComment: function () {
        var _that = this, comment = {},
            $form = $(_.template($('#comment-form-template').html(), {}));
        if (_that.$el.find('form').length > 0) {
            return false;
        }
        $form.insertBefore(_that.$el.find('.subcomments:first')).find('textarea').focus();
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
            if (_that.sublistState === 'hidden') {
                _that.showReplies();
            }
            return false;
        });
        return false;
    },
    
    voteUp: function () {
        var _that = this,
            vStart = _that.model.get('upvotes'),
            vTotal = _that.model.get('total_votes');
        sendAjaxRequest('POST', '/rest/votes/', {
            data: {
                vote: 'up',
                comment: _that.model.id
            },
            success: function (resp) {
                if (resp.success === true) {
                    _that.model.set('upvotes', ++vStart);
                    _that.model.set('total_votes', ++vTotal);
                    _that.render();
                    display_alert(resp.message, 'success');
                } else {
                    display_alert(resp.message, 'danger');
                }
            },
            error: function (err) {
                display_alert(gettext('Something somewhere went terribly wrong!'), 'danger');
            }
        });
        return false;
    },
    
    voteDown: function () {
        var _that = this,
            vStart = _that.model.get('downvotes'),
            vTotal = _that.model.get('total_votes');
        sendAjaxRequest('POST', '/rest/votes/', {
            data: {
                vote: 'down',
                comment: _that.model.id
            },
            success: function (resp) {
                if (resp.success === true) {
                    _that.model.set('downvotes', ++vStart);
                    _that.model.set('total_votes', --vTotal);
                    _that.render();
                    display_alert(resp.message, 'success');
                } else {
                    display_alert(resp.message, 'danger');
                }
            },
            error: function (err) {
                display_alert('Something somewhere went terribly wrong!', 'danger');
            }
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
                submit_date: moment().format(),
                parent: parentId
            };
            comment = new commentlist.Comment(formData);
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
        var CommentView = new commentlist.CommentView({
            model: item
        });
        $(CommentView.render().el).prependTo(this.$el);
    }
});
//
// List all comments view
// -------------------------------------------------------------------------
commentlist.CommentlistView = Backbone.View.extend({
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
        comment = new commentlist.Comment(formData);
        comment.url = '/rest/comments/';
        _that.collection.add(comment);
        $.ajaxSetup({
            headers: {'X-CSRFToken': getCookie('csrftoken')}
        });   
        comment.save();
        incrementCommentCounter();
    },
    
    initialize: function (initialComments) {
        var _that = this;
        _that.collection = new commentlist.Commentlist(initialComments);
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
        var CommentView = new commentlist.CommentView({
            model: item
        });
        $(CommentView.render().el)
            .insertAfter(this.$el.find('.commentformarea'));
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