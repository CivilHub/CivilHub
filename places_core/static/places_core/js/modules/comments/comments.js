//
// comments.js
// ===========

// Initializes the comment application.

require(['jquery',
         'js/modules/comments/comment-list-view'],

function ($, CommentList) {
    
"use strict";

$(document).ready(function () {

  // We create a list of comments

  var comments = new CommentList({
    totalRecords: 'count',
    label: $('#target-label').val(),
    ct: $('#target-type').val(),
    id: $('#target-id').val()
  });
  
  // Show/Hide comments

  $('.comment-toggle').on('click', function (e) {
    e.preventDefault();
    if ($('#comments').is(':visible')) {
      $('#comments').slideUp('fast', function () {
        $('.comment-toggle').text(gettext('Show comments'));
      });
    } else {
      $('#comments').slideDown('fast', function () {
        $('.comment-toggle').text(gettext('Hide comments'));
      });
    }
  });

  // Sort the comments in a proper sequence

  $('.change-order-link').on('click', function (e) {
    e.preventDefault();
    comments.filter($(this).attr('data-order'));
  });
});
});