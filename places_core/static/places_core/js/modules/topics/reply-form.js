//
// Forum scripts.
// ==============
//

require(['jquery', 'bootstrap'],

function ($) {
    
    "use strict";
    
    var editor = null,
    
        reply  = window.CIVIL_REPLY_URL;

    editor = $('#id_content');

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
            quotedTxt = $entry.find('.entry-content').html();

        evt.preventDefault();
        $('#reply-form').attr('action', reply).slideDown('fast');
        editor.html(quoteEntry + ' wrotes: ' + quotedTxt);
    });

    // Edit existing entry
    // -------------------------------------------------------------------------
    $('.link-entry-edit').bind('click', function (e) {
        var $entry = $(this).parents('.reply-entry'),
            content= $entry.find('.entry-content').html(),
            target = $(this).attr('href');
        
        e.preventDefault();
        $('#reply-form').attr('action', target).slideDown('fast', function () {
            editor.text(content);
            $('html, body')
                .scrollTop($('#reply-form').position().top + 800);
        });
    });

});