//
// commentView.js
// ==============
// First-level single comment view.
define(['jquery',
        'underscore',
        'backbone',
        'js/comments/subcommentView'],

function ($, _, Backbone, SubcommentView) {
    "use strict";
    
    var CommentView = Backbone.View.extend({
        
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
            'click .vote-down-link': 'voteDown'
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
                        new SubcommentView(replies, 
                            _that.$el.find('.subcomments'));
                });
            } else {
                _that.$el.find('.show-replies').hide();
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
        
        update: function (attrs, callback, params) {
            sendAjaxRequest('PATCH', '/rest/comments/'+this.model.get('id')+'/', {
                data: attrs,
                success: function (resp) {
                    display_alert(resp.message, resp.level);
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
                $content  = _that.$el.find('.comment-content:first'),
                $controls = _that.$el.find('.comment-controls:first'),
                content = $content.html(),
                $editor = $('<textarea></textarea>'),
                $cancel = $('<button></button>'),
                $submit = $('<button></button>');
            $content.empty();
            $controls.css('display', 'none');
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
                    _that.model.set('submit_date', moment().format());
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
            _that.$el.find('.show-replies').show();
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
                    display_alert(gettext('Something somewhere went terribly wrong!'), 'danger');
                }
            });
            return false;
        }
    });
    
    return CommentView;
});