//
// Forum scripts.
// ==============
//

require(['jquery'],

function ($) {
    
    "use strict";
    
    var editor = null,
        reply  = window.CIVIL_REPLY_URL;

    editor = $('#id_content').data('editor');

    $('.entry-controls').find('a').tooltip();

    // Add new entry.
    // -------------------------------------------------------------------------
    $('.reply-entry-btn').on('click', function (evt) {
        evt.preventDefault();
        $('#reply-form').attr('action', reply).slideToggle('fast');
    });

    // Reply with quotation of previous entry.
    // -------------------------------------------------------------------------
    $('.quote-reply-link').on('click', function (evt) {
        var $entry = $(this).parents('.reply-entry'),
            quoteEntry = $entry.find('.user-window-toggle').text(),
            quotedTxt = '<em>' + $entry.find('.entry-content').html() + '</em>',
            range = editor.createRange();
        evt.preventDefault();
        $('#reply-form').attr('action', reply).slideDown('fast');
        editor.setData('<h3>' + quoteEntry + ' wrotes:</h3>' + quotedTxt + '<p></p>');
        try {
            range.moveToElementEditablePosition(p);
            range.select();
        } catch (e) {
            console.log(e);
        }
    });

    // Edit existing entry
    // -------------------------------------------------------------------------
    $('.link-entry-edit').bind('click', function (e) {
        var $entry = $(this).parents('.reply-entry'),
            content= $entry.find('.entry-content').html(),
            target = $(this).attr('href');
        console.log(content);
        e.preventDefault();
        $('#reply-form').attr('action', target).slideDown('fast', function () {
            editor.setData(content);
            $('html, body')
                .scrollTop($('#reply-form').position().top + 800);
        });
    });

});