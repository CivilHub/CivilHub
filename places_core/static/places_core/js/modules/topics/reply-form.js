//
// Forum scripts.
// ==============

// Simple script to handle reply form on single discussion page. It needs some
// fixes - mainly when we use 'cite' option or editing content. There is also
// some problem with links in response content.

require(['jquery',
         'bootstrap'],

function ($) {

  "use strict";

  var editor = null;

  var reply  = window.CIVIL_REPLY_URL;

  editor = $('#id_content');

  $('.entry-controls').find('a').tooltip();

  // Add new entry.
  // ---------------------------------------------------------------------------

  $('.reply-entry-btn').on('click', function (evt) {
    evt.preventDefault();
    $('#reply-form').attr('action', reply).slideToggle('fast');
  });

  // Reply with quotation of previous entry.
  // ---------------------------------------------------------------------------

  $('.quote-reply-link').on('click', function (evt) {
    var $entry = $(this).parents('.reply-entry');
    var quoteEntry = $entry.find('.user-window-toggle').text();
    var quotedTxt = $entry.find('.entry-content').text();

    evt.preventDefault();
    $('#reply-form').attr('action', reply).slideDown('fast');
    editor.html(quoteEntry + ' wrotes: ' + quotedTxt);
  });

  // Edit existing entry
  // ---------------------------------------------------------------------------

  $('.link-entry-edit').bind('click', function (e) {
    var $entry = $(this).parents('.reply-entry');
    var content = $entry.find('.entry-content').text();
    var target = $(this).attr('href');

    e.preventDefault();
    $('#reply-form').attr('action', target).slideDown('fast', function () {
      editor.text(content);
      $('html, body')
          .scrollTop($('#reply-form').position().top + 800);
    });
  });

});
