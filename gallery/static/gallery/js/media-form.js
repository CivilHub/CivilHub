//
// Script to handle location gallery page.
// -----------------------------------------------------------------------------
(function ($) {    
"use strict";

$('#gallery a').colorbox({
    rel: 'gal',
    maxWidth: "90%",
    maxHeight: "80%"
});

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
    
})(jQuery);