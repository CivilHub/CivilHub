//
// comment-list-view.js
// ====================
// Główny widok dla komentarzy - obsługuje całą listę.
//

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/utils/utils',
        'js/modules/comments/comment-collection',
        'js/modules/comments/comment-view',
        'js/modules/comments/comment-model'],

function ($, _, Backbone, utils, CommentCollection, CommentView, CommentModel) {
    
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
        
        // Referencje do widoków komentarzy. Wspólnym kluczem jest ID modelu.
        items: {}, 
        
        initialize: function () {
            
            var self = this; // FIXME: pozbyć się tego
            
            // Konieczne ze względu na Django CSRF Protection
            $.ajaxSetup({
                headers: {'X-CSRFToken': utils.getCookie('csrftoken')}
            });
            
            // Wywołanie paginowalnej kolekcji, ustalenie liczby elementów na
            // jednej stronie i wyświetlenie pierwszej strony.
            this.collection = new CommentCollection();
            this.collection.state.pageSize = window.pageSize;
            this.collection.fetch({
                success: function (collection, response, method) {
                    self.render();
                }
            });
            
            // Dodawanie nowych komentarzy (nie zagnieżdżonych)
            $('#user-comment-form').on('submit', function (e) {
                e.preventDefault();
                this.addComment();
            }.bind(this));
            
            // Usuwamy referencje widoków kiedy resetujemy kolekcję/wczytujemy nową
            this.listenTo(this.collection, 'sync', this.cleanup);
            
            // TEST!!!
            CivilApp.testApp = this;
            $(document).on('click', function (e) {
                console.log(this.collection);
            });
        },
        
        render: function () {
            // Wyświetla listę komentarzy.
            this.collection.each(function (item) {
                this.renderComment(item);
            }, this);
            // Off i on są tutaj konieczne ze względu na problemy z późniejszym
            // doczytywaniem listy. Enable lazy-loading on page scrolling
            $(window).off('scroll');
            $(window).scroll(function() {
                if($(window).scrollTop() + $(window).height() == $(document).height()) {
                    this.nextPage();
                }
            }.bind(this));
            if (this.collection.length <= CivilApp.maxComments) {
                alert("Yes, it's lower");
                $('#comment-order-controls').hide();
            }
        },
        
        renderComment: function (item) {
            // Funkcja dodaje komentarze na końcu listy, używana podczas inicja-
            // lizacji i resetowania kolekcji.
            var comment = new CommentView({model:item});
            comment.parentView = this;
            $(comment.render().el).appendTo(this.$el);
            this.items[item.get('id')] = comment;
        },
        
        prependComment: function (item) {
            // Funkcja dodaje komentarze na początku listy, np. kiedy tworzymy
            // nowy.
            var comment = new CommentView({model:item});
            $(comment.render().el).prependTo(this.$el);
        },
        
        addComment: function () {
            var self = this; // FIXME: pozbyć się tego
            if ($('#comment').val().length <= 0) {
                alert(gettext("Comment cannot be empty"));
                return false;
            }
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
            // Reset
            this.$el.empty();
            // Aplikujemy jeden z filtrów: `votes`, `submit_date`, `-submit_date`.
            this.collection.state.currentPage = null;
            _.extend(this.collection.queryParams, {
                filter: filter
            });
        },
        
        nextPage: function () {
            // Pobranie następnej strony po przewinięciu ekranu. Ta funkcja cza-
            // sami rzuca błąd lub zwraca 404, ale nie należy się tym przejmować :)
            // Backbone.pageableCollection ma jakiś błąd, który sprawia, że nie
            // można polegać na funkcji hasNextPage.
            var self = this,
                model = null;
            
            this.collection.getNextPage({
                // Pobieramy nową stronę i wyświetlamy komentarze.
                success: function (collection, response, method) {
                    _.each(response.results, function (item) {
                        var model = new CommentModel(item);
                        self.renderComment(model);
                    });
                }
            });
        },
        
        cleanup: function () {
            // Metoda "czyści" listę widoków powiązanych z modelami w kolekjci
            this.items = {};
        }
    });
    
    return CommentListView;
});