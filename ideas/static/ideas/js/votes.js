(function ($) {
    "use strict";
    $('.vote-btn').on('click', function () {
        var formData = {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                idea: $('#idea-metadata').val(),
                vote: $(this).attr('data-vote')
            },
            callback = function (data) {
                display_alert('Thanks for voting!', 'success');
            };
        $.ajax({
            type: 'POST',
            url: '/ideas/vote/',
            data: formData,
            success: callback
        });
    });
})(jQuery);