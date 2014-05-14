(function ($) {
    "use strict";
    //
    // Form elements
    // -------------------------------------------------------------------------
    //
    var editor = CKEDITOR.replace('id_description');
    $('#id_tags').tagsInput({
        autocomplete_url: '/rest/tags/',
    });
    //
    // Dynamic question form
    // -------------------------------------------------------------------------
    //
    function AnswerForm(id, question) {
        return {
            id: id,
            question: question,
            $el: $('<div class="answer-entry"></div>'),
            template: _.template($('#answer-entry-tpl').html()),
            render: function () {
                var _that = this;
                _that.$el.html(_that.template({
                    id: id,
                    qid: _that.question.id
                }));
                return _that.$el;
            }
        }
    }
    function QuestionForm(id) {
        return {
            id: id,
            $el: $('<div class="question-entry"></div>'),
            answers: 0,
            template: _.template($('#question-entry-tpl').html()),
            render: function () {
                var _that = this;
                _that.$el.html(_that.template({id:id}));
                _that.$el.find('button').tooltip().bind('click', function () {
                    _that.addAnswer();
                });
                _that.$el.find('.remove-btn').on('click', function () {
                    _that.deleteSelf();
                });
                return _that.$el;
            },
            addAnswer: function () {
                var id = $('.answer-entry').length + 1,
                    a = new AnswerForm(id, this);
                this.$el.append(a.render());
            },
            deleteSelf: function () {
                var _that = this;
                _that.$el.fadeOut('fast', function () {
                    _that.$el.empty().remove();
                });
            }
        }
    }
    function createQuestion () {
        var id = $('.question-entry').length + 1,
            q = new QuestionForm(id);
        $('#poll-question-form').append(q.render());
        q.addAnswer();
    }
    //
    // Add initial question form
    // -------------------------------------------------------------------------
    //
    $(document).ready(function () {
        createQuestion();
        $('.add-question-btn').tooltip().bind('click', function () {
            createQuestion();
        });
    });
})(jQuery);