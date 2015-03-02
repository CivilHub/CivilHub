//
// comments.js
// ===========
// Inicjalizuje aplikację komentarzy.
//

require(['jquery',
         'js/modules/comments/comment-list-view'],

function ($, CommentList) {
    
    "use strict";
    
    // Tworzymy listę komentarzy.
    var comments = new CommentList();
    
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
    
    // Sortuj komentarze w odpowiedniej kolejności
    $('.change-order-link').on('click', function (e) {
        e.preventDefault();
        comments.filter($(this).attr('data-order'));
    });
});