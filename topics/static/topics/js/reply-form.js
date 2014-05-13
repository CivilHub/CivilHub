(function ($) {
    "use strict";
    var editor = CKEDITOR.replace('id_content');
    $('.entry-controls').find('a').tooltip();
    $('.reply-entry-btn').on('click', function (evt) {
        evt.preventDefault();
        $('#reply-form').slideToggle('fast');
    });
    $('.quote-reply-link').on('click', function (evt) {
        var $entry = $(this).parents('.reply-entry'),
            quoteEntry = $entry.find('.news-user-avatar').attr('alt'),
            quotedTxt = '<em>' + $entry.find('.entry-content').html() + '</em>';
        evt.preventDefault();
        $('#reply-form').slideDown('fast');
        editor.setData('<h3>' + quoteEntry + ' wrotes:</h3>' + quotedTxt);
    });
})(jQuery);