//
// comment-list-view.js
// ====================
// Główny widok dla komentarzy - obsługuje całą listę.
//

define(['jquery',
        'underscore',
        'backbone',
        'js/comments/comment-collection',
        'js/comments/comment-view'],

function ($, _, Backbone, CommentCollection, CommentView) {
    
    "use strict";
    
    var incrementCommentCount = function () {
        // Funkcja inkrementuje informację o liczbie komentarzy.
        var $counter = $('.comment-count'),
            value = parseInt($counter.text(), 10),
            nVal = 1;
        
        if (!_.isNaN(value)) {
            nVal = ++value;
        }
        
        $counter.text(nVal);
    };
    
    var CommentListView = Backbone.View.extend({
        
        el: '#comments',
        
        initialize: function () {
            // Konieczne ze względu na Django CSRF Protection
            $.ajaxSetup({
                headers: {'X-CSRFToken': getCookie('csrftoken')}
            });
            
            // Wywołanie paginowalnej kolekcji i ustalenie liczby elementów na
            // jednej stronie.
            this.collection = new CommentCollection();
            this.collection
                .setPageSize(parseInt($('#comment-page-size').val(), 10));
            
            // Dodawanie nowych komentarzy (nie zagnieżdżonych)
            $('#user-comment-form').on('submit', function (e) {
                e.preventDefault();
                this.addComment();
            }.bind(this));
            
            // Wyświetl nowo dodane/wczytane komentarze
            this.listenTo(this.collection, 'add', this.renderComment);
        },
        
        render: function () {
            this.collection.each(function (item) {
                this.renderComment(item);
            }, this);
        },
        
        renderComment: function (item) {
            var comment = new CommentView({model:item});
            $(comment.render().el).appendTo(this.$el);
        },
        
        prependComment: function (item) {
            var comment = new CommentView({model:item});
            $(comment.render().el).prependTo(this.$el);
        },
        
        addComment: function () {
            // Utworzenie nowego komentarza - z formularza pobierany jest sam
            // tekst, resztę dodają skrypty i server.
            this.collection.create({comment:$('#comment').val()});
            // Wyczyść formularz.
            $('#comment').val('');
            // Zwiększ liczbę komentarzy w oknie informacyjnym
            incrementCommentCount();
        }
    });
    
    return CommentListView;
});