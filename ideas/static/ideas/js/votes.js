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
            callback = function (data) {
                data = JSON.parse(data);
                if (data.success === true) {
                    display_alert(data.message, 'success');
                    $votes.html(data.votes);
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