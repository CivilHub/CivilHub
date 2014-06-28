(function ($) {
    "use strict";
    var editor = null;
    $('#id_content').customCKEditor('custom');
    editor = $('#id_content').data('editor');
    console.log(editor);
    $('.entry-controls').find('a').tooltip();
    $('.reply-entry-btn').on('click', function (evt) {
        evt.preventDefault();
        $('#reply-form').slideToggle('fast');
    });
    $('.quote-reply-link').on('click', function (evt) {
        var $entry = $(this).parents('.reply-entry'),
            quoteEntry = $entry.find('.user-window-toggle').text(),
            quotedTxt = '<em>' + $entry.find('.entry-content').html() + '</em>',
            range = editor.createRange();
        evt.preventDefault();
        $('#reply-form').slideDown('fast');
        editor.setData('<h3>' + quoteEntry + ' wrotes:</h3>' + quotedTxt + '<p></p>');
        range.moveToElementEditablePosition(p);
        range.select();
    });
})(jQuery);