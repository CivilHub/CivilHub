//
// comments.js
// ===========
// Run comments application.
require(['jquery',
         'js/comments/commentCollection',
         'js/comments/commentListView'],

function ($, CommentCollection, CommentListView) {
    "use strict";

    // Set apps url
    var cType = $('#target-type').val(),
    
        cId = $('#target-id').val(),
        
        cPrefix = $('#target-label').val(),
        
        url = ['/rest/comments?content-label=',
               cPrefix,
               '&content-type=',
               cType,
               '&content-id=',
               cId].join('');

    //
    // Start Application.
    // -----------------------------------------------------------------------------
    $.get(url, function (comments) {
        var commentCollection = new CommentCollection(comments);
        var comments = new CommentListView({
            collection: commentCollection
        });
    });
    //
    // Bind show/hide comment controls event.
    // -----------------------------------------------------------------------------
    $(document).on('mouseover', '.comment', function (e) {
        e.stopPropagation();
        $(this).find('.comment-controls:first').css('opacity', 1);
    });
    $(document).on('mouseout', '.comment', function () {
        $(this).find('.comment-controls').css('opacity', 0);
    });
});