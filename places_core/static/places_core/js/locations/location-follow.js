//
// location-follow.js
// ==================
// Follow/unfollow locations
require(['jquery'],

function ($) {
    "use strict";
    //
    // Follow location button
    // ----------------------
    //
    $(document).on('click', '.btn-follow-location', function () {
        var $btn = $(this);
        $.ajax({
            type: 'POST',
            url: '/add_follower/' + $btn.attr('data-location-id'),
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.success === true) {
                    message.success(resp.message);
                    $btn.fadeOut('fast', function () {
                        $btn.removeClass('btn-follow-location btn-success')
                            .addClass('btn-unfollow-location btn-danger')
                            .text(gettext('Stop following'))
                            .fadeIn('fast');
                    });
                } else {
                    message.alert(resp.message);
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
            url: '/remove_follower/' + $btn.attr('data-location-id'),
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.success === true) {
                    $btn.fadeOut('fast', function () {
                        $btn.removeClass('btn-unfollow-location btn-danger')
                            .addClass('btn-follow-location btn-success')
                            .text(gettext('Follow'))
                            .fadeIn('fast');
                    });
                    message.success(resp.message);
                } else {
                    message.alert(resp.message);
                }
            }
        });
    });
});