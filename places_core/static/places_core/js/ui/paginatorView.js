//
// paginatorView.js
// ================
// Simple Backbone view to display navigation for PageableCollection.
// 
// Inicjalizator klasy przyjmuje parametr w postaci obiektu zawierającego
// opcje. Większość z nich jest wymagana, nie zdążyłem też wprowadzić
// należytego wyłapywania błędów. Wymagane parametry to:
//   - count:   Całkowita liczba rezultatów (count w odpowiedzi REST servera)
//   - perPage: Ilość elementów na stronę, trzeba to wprowadzić ręcznie
//   - targetCollection: Backbone's PageableCollection instance
//   - data (optional) : Additional query params
//
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    var PaginatorView = Backbone.View.extend({
        
        tagName: 'ul',
        
        className: 'pagination',
        
        template: _.template($('#paginator-tpl').html()),
        
        initialize: function (collection) {
            this.collection = collection;
        },
        
        render: function () {
            this.$el.html(this.template(this));
            return this;
        }
    });
    
    return PaginatorView;
});