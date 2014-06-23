(function ($) {
"use strict";
//
// Handle voting on list page.
// -----------------------------------------------------------------------------
$('.vote-btn').on('click', function () {
    var formData = {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            idea: $(this).attr('data-target-id'),
            vote: $(this).attr('data-vote')
        },

        $votes = $(this).parents('.idea-votes:first')
            .find('.votes:first'),

        $counter = $(this).parents('.idea-votes:first')
            .find('.idea-vote-count:first'),

        votes = parseInt($counter.text(), 10) || 0,

        callback = function (data) {
            data = JSON.parse(data);
            if (data.success === true) {
                display_alert(data.message, 'success');
                $votes.html(data.votes);
                if (!_.isNaN(votes)) {
                    $counter.text(++votes);
                } else {
                    $counter.text(0);
                }
            } else {
                display_alert(data.message, 'danger');
            }
        };

    $.ajax({
        type: 'POST',
        url: '/ideas/vote/',
        data: formData,
        success: callback
    });
});
//
// Get list of users and their votes.
// -----------------------------------------------------------------------------
var voteCounter = function (ideaId) {
    // Put Backbone MVC in bootstrap modal window.
    var getVotes = function (id, callback) {
            var data = {};
            sendAjaxRequest('GET', '/rest/idea_votes/', {
                data: {pk: id},
                success: function (resp) {
                    if (typeof(callback) === 'function') {
                        callback(resp);
                    }
                },
                error: function (err) {
                    console.log(err);
                }
            });
        },

        VoteModel = Backbone.Model.extend({}),

        VoteView = Backbone.View.extend({
            tagName:   'li',
            className: 'entry',
            template:  _.template($('#vote-counter-entry').html()),
            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                return this;
            }
        }),

        CountList = Backbone.Collection.extend({
            model: VoteModel
        }),

        Counter = Backbone.View.extend({
            el: '#vote-counter-modal',
            initialize: function () {
                var that = this;
                getVotes(ideaId, function (votes) {
                    that.collection = new CountList(votes);
                    that.$entries = that.$el.find('.modal-body');
                    that.$entries.empty();
                    that.render();
                });
            },
            render: function () {
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
                this.$el.modal('show');
            },
            renderEntry: function (item) {
                var entry = new VoteView({
                    model: item
                });
                $(entry.render().el).appendTo(this.$entries);
            }
        });

    return new Counter;
};
$('.idea-vote-count').bind('click', function () {
    var cc = voteCounter($(this).attr('data-target'));
});

})(jQuery);