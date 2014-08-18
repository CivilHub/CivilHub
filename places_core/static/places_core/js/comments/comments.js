//
// comments.js
// ===========
// Inicjalizuje aplikację komentarzy.
//

require(['jquery',
         'js/comments/comment-list-view'],

function ($, CommentList) {
    
    "use strict";
    
    // Tworzymy listę komentarzy.
    var comments = new CommentList();
    
    // Przycisk "Pokaż więcej" - wczytanie kolejnej strony komentarzy.
    $('.comment-show-btn').on('click', function (e) {
        e.preventDefault();
        if (comments.collection.hasNextPage()) {
            comments.collection.getNextPage();
        }
    });
    
    // Pokaż/Ukryj komentarze
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
});