(function ($) {
    "use strict";
    $('.vote-btn').on('click', function () {
        var formData = {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                idea: $('#idea-metadata').val(),
                vote: $(this).attr('data-vote')
            },
            callback = function (data) {
                data = JSON.parse(data);
                if (data.success === true) {
                    display_alert('Thanks for voting!', 'success');
                    $('#votes').html(data.votes);
                } else {
                    display_alert('Operation failed', 'danger');
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