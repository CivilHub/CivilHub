//
// Script to handle location gallery page.
// -----------------------------------------------------------------------------
(function ($) {    
"use strict";

/*
$('.gallery-item').colorbox({
    rel: 'gal',
    maxWidth: "90%",
    maxHeight: "80%"
});*/


$('.media-form-toggle').on('click', function (e) {
    e.preventDefault();
    $('#media-form').slideDown('fast');
});

$('.thumbnail').on('mouseover', function (e) {
    $(this)
        .find('.item-controllers')
        .css('display', 'block')
        .stop(true).animate({
            opacity: 1
        }, {
            duration: 'slow',
            queue: false
        });

    $(this).one('mouseout', function (e) {
        $(this).find('.item-controllers').stop(true).animate({
            opacity: 0
        }, {
            duration: 'slow',
            queue: false,
            done: function () {
                $(this).css('display', 'none');
            }
        });
    });
});

$('.item-control-btn').on('click', function (e) {
    var tId = $(this).attr('data-target'),
        $el = $(this).parents('.file-entry:first');
    e.preventDefault();
    sendAjaxRequest('DELETE', '/rest/galleries/' , {
        data: {pk: tId},
        success: function (resp) {
            display_alert(resp.message, resp.level);
            $el.fadeOut('fast', function () {
                $(this).empty().remove();
            });
        },
        error: function (err) {
            console.log(err);
        }
    });
});
    
})(jQuery);