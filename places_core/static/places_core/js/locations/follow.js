//
// follow.js
// =========
// Obsługa przycisków 'follow location' i 'stop following'.
//
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
            url: '/locations/add_follower/' + $btn.attr('data-location-id'),
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.success === true) {
                    message.success(resp.message);
                    $btn.fadeOut('fast', function () {
                        $btn.removeClass('btn-follow-location')
                            .addClass('btn-unfollow-location')
                            .text(gettext('You are following'))
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
            url: '/locations/remove_follower/' + $btn.attr('data-location-id'),
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function (resp) {
                resp = JSON.parse(resp);
                if (resp.success === true) {
                    $btn.fadeOut('fast', function () {
                        $btn.removeClass('btn-unfollow-location')
                            .addClass('btn-follow-location')
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