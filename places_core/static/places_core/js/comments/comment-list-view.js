//
// comment-list-view.js
// ====================
// Główny widok dla komentarzy - obsługuje całą listę.
//

define(['jquery',
        'underscore',
        'backbone',
        'js/comments/comment-collection',
        'js/comments/comment-view',
        'js/comments/comment-model'],

function ($, _, Backbone, CommentCollection, CommentView, CommentModel) {
    
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
            
            var self = this; // FIXME: pozbyć się tego
            
            // Konieczne ze względu na Django CSRF Protection
            $.ajaxSetup({
                headers: {'X-CSRFToken': getCookie('csrftoken')}
            });
            
            // Wywołanie paginowalnej kolekcji, ustalenie liczby elementów na
            // jednej stronie i wyświetlenie pierwszej strony.
            this.collection = new CommentCollection();
            this.collection
                .setPageSize(parseInt($('#comment-page-size').val(), 10));
            this.collection.fetch({
                success: function () {
                    self.render();
                }
            });
            
            // Dodawanie nowych komentarzy (nie zagnieżdżonych)
            $('#user-comment-form').on('submit', function (e) {
                e.preventDefault();
                this.addComment();
            }.bind(this));
        },
        
        render: function () {
            // Wyświetla listę komentarzy.
            this.collection.each(function (item) {
                this.renderComment(item);
            }, this);
            // Off i on są tutaj konieczne ze względu na problemy z późniejszym
            // doczytywaniem listy.
            $('.comment-show-btn').off('click');
            $('.comment-show-btn').on('click', function (e) {
                e.preventDefault();
                this.nextPage();
            }.bind(this));
        },
        
        renderComment: function (item) {
            // Funkcja dodaje komentarze na końcu listy, używana podczas inicja-
            // lizacji i resetowania kolekcji.
            var comment = new CommentView({model:item});
            $(comment.render().el).appendTo(this.$el);
        },
        
        prependComment: function (item) {
            // Funkcja dodaje komentarze na początku listy, np. kiedy tworzymy
            // nowy.
            var comment = new CommentView({model:item});
            $(comment.render().el).prependTo(this.$el);
        },
        
        addComment: function () {
            var self = this; // FIXME: pozbyć się tego
            // Utworzenie nowego komentarza - z formularza pobierany jest sam
            // tekst, resztę dodają skrypty i server.
            this.collection.create({comment:$('#comment').val()}, {
                success: function (model, resp) {
                    self.prependComment(model);
                }
            });
            // Wyczyść formularz.
            $('#comment').val('');
            // Zwiększ liczbę komentarzy w oknie informacyjnym
            incrementCommentCount();
        },
        
        filter: function (filter) {
            var self = this; // FIXME: pozbyć się tego
            // Reset
            this.$el.empty();
            this.collection.reset();
            // Resetujemy aktualną stronę, aby uniknąć pobierania dalszych na
            // samym początku.
            this.collection.state.currentPage = 1;
            // Aplikujemy jeden z filtrów: `votes`, `submit_date`, `-submit_date`.
            _.extend(this.collection.queryParams, {
                filter: filter
            });
            // Pobieramy nową kolekcję i wyświetlamy elementy.
            this.collection.fetch({
                success: function () {self.render();}
            });
        },
        
        nextPage: function () {
            // Pobranie następnej strony po kliknięciu przycisku 'więcej'
            var self = this, // FIXME: pozbyć się tego
                model = null;
            if (this.collection.hasNextPage()) {
                this.collection.getNextPage({
                    // Pobieramy nową stronę i wyświetlamy komentarze.
                    success: function (collection, response, method) {
                        _.each(response.results, function (item) {
                            var model = new CommentModel(item);
                            self.renderComment(model);
                        });
                    }
                });
            }
        }
    });
    
    return CommentListView;
});