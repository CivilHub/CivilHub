(function ($) {
    "use strict";
    //
    // Follow location button
    // ----------------------
    //
    $(document).on('click', '.btn-follow-location', function () {
        var $btn = $(this);
        $.ajax({
            type: 'POST',
            url: 'locations/add_follower/' + $btn.attr('data-location-id'),
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.success === true) {
                    display_alert(resp.message, 'success');
                    $btn.fadeOut('fast', function () {
                        $btn.removeClass('btn-follow-location btn-success')
                            .addClass('btn-unfollow-location btn-danger')
                            .text('Stop following')
                            .fadeIn('fast');
                    });
                } else {
                    display_alert(resp.message, 'danger');
                }
            }
        });
    });
    //
    // Unfollow location button
    // ----------------------
    //
    $(document).on('click', '.btn-unfollow-location', function () {
        var $btn = $(this);
        $.ajax({
            type: 'POST',
            url: 'locations/remove_follower/' + $btn.attr('data-location-id'),
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.success === true) {
                    $btn.fadeOut('fast', function () {
                        $btn.removeClass('btn-unfollow-location btn-danger')
                            .addClass('btn-follow-location btn-success')
                            .text('Follow')
                            .fadeIn('fast');
                    });
                    display_alert(resp.message, 'success');
                } else {
                    display_alert(resp.message, 'danger');
                }
            }
        });
    });
})(jQuery);