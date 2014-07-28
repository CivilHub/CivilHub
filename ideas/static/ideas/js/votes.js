//
// votes.js
// ========
//
// Handles user's votes for ideas.
//
var CivilApp = CivilApp || {};
//
// Handle voting on list page.
// -----------------------------------------------------------------------------
$(document).delegate('.vote-btn', 'click', function () {
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
CivilApp.voteCounter = function (ideaId) {
    // Put Backbone MVC in bootstrap modal window.
    var getVotes = function (id, callback) {
            sendAjaxRequest('GET', '/rest/idea_votes/', {
                data: {pk: id},
                success: function (resp) {
                    if (typeof(callback) === 'function') {
                        callback(resp);
                    }
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
                this.markLabel(this.model.get('vote'));
                return this;
            },
            markLabel: function (vote) {
                var $label = this.$el.find('.vote-result-label'),
                    $labelTxt = $label.find('.fa');
                if (vote) {
                    $label.addClass('label-success');
                    $labelTxt.addClass('fa-arrow-up');
                } else {
                    $label.addClass('label-danger');
                    $labelTxt.addClass('fa-arrow-down');
                }
            }
        }),

        CountList = Backbone.Collection.extend({
            model: VoteModel
        }),

        Counter = Backbone.View.extend({
            el: '#vote-counter-modal',
            initialize: function () {
                var that = this,
                    positive_votes = [],
                    negative_votes = [];
                getVotes(ideaId, function (votes) {
                    _.each(votes, function (item) {
                        console.log(item);
                        if (item.vote) {
                            positive_votes.push(item);
                        } else {
                            negative_votes.push(item);
                        }
                    });
                    that.positive_collection = new CountList(positive_votes);
                    that.negative_collection = new CountList(negative_votes);
                    that.$pEntries = that.$el.find('.positive-votes');
                    that.$pCounter = that.$el.find('.positive-counter');
                    that.$pEntries.empty();
                    that.$nEntries = that.$el.find('.negative-votes');
                    that.$nCounter = that.$el.find('.negative-counter');
                    that.$nEntries.empty();
                    that.render();
                });
            },
            render: function () {
                this.positive_collection.each(function (item) {
                    this.renderPositiveEntry(item);
                }, this);
                this.$pCounter.text(this.positive_collection.length);
                this.negative_collection.each(function (item) {
                    this.renderNegativeEntry(item);
                }, this);
                this.$nCounter.text(this.negative_collection.length);
                this.$el.modal('show').data('voteCounter', this);
            },
            renderPositiveEntry: function (item) {
                var entry = new VoteView({
                    model: item
                });
                $(entry.render().el).appendTo(this.$pEntries);
            },
            renderNegativeEntry: function (item) {
                var entry = new VoteView({
                    model: item
                });
                $(entry.render().el).appendTo(this.$nEntries);
            }
        });

    return new Counter;
};
