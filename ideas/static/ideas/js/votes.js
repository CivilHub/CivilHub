(function ($) {
    "use strict";
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
})(jQuery);