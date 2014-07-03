//
// simple-paginator.js
// ===================
//
// Paginacja wyników zapytań do widoków typu REST nie powiązanych z Django
// REST Framework (tzn. korzystających bezpośrednio z widoków Django).
// Ponieważ chcemy przesyłać wyniki w nieco innej formie, nie możemy tutaj
// skorzystać z rest-paginator.js.
//
// Najczęściej wykorzystywane opcje to 'currentPage', czyli numer aktualnie
// przeglądanej strony, 'totalPages', czyli całkowita liczba stron oraz callback
// zwracany jako sukces po kliknięciu na któryś z lnków w paginacji.
//
// Przykład:
//
//   var my_paginator = CivilApp.SimplePaginator({
//       currentPage: 5,
//       totalPages: 35,
//       onChange: function (page) {alert(page);}
//   });
//
var CivilApp = CivilApp || {};

//
// Helper functions.
// -----------------------------------------------------------------------------
//

// Funkcja pobierająca dodatkowe dane z formularza 'search'.
// ---------------------------------------------------------
var getSearchText = function () {
    var $field = $('#haystack'),
        txt = $field.val();
    
    if (_.isUndefined(txt) || txt.length <= 1) {
        return '';
    }
    
    return txt;
};

//
// Wczytanie wybranych opcji.
// ---------------------------
// Sprawdzenie aktywnych elementów (klikniętych linków)
// w celu "pozbierania" opcji wyszukiwarki.
// 
var getListOptions = function () {
    var $sel = $('.list-controller'),
        opts = {},
        optType = null,
        optValue = null;
    
    $sel.each(function () {
        var $this = $(this);
        
        if ($this.hasClass('active')) {
            optType = $this.attr('data-control');
            optValue = $this.attr('data-target');
            opts[optType] = optValue;
        }
    });
    
    opts['haystack'] = getSearchText();
    
    return opts;
};

//
// Paginator
// -----------------------------------------------------------------------------
//
CivilApp.SimplePaginator = function (options) {
    
    var defaults = {
            startPage  : 1,
            currentPage: 1,
            totalPages : 10,
            className  : 'pagination',
            activeClass: 'active',
            firstLabel : '<<',
            lastLabel  : '>>',
            prevLabel  : '<',
            nextLabel  : '>',
            onChange: function (page) {
                console.log("Simple paginator selected page: " + page);
            }
        },
    
        options = $.extend(defaults, options),
        
        PageModel = Backbone.Model.extend({}),
        
        Page = Backbone.View.extend({
            tagName: 'li',
            
            template: _.template('<a href="<%= page %>"><%= text %></a>'),
            
            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                if (this.model.get('page') == options.currentPage)
                    this.$el.addClass(options.activeClass);
                return this;
            }
        }),
        
        Pages = Backbone.Collection.extend({
            model: PageModel
        }),
        
        Paginator = Backbone.View.extend({
        
            fillCollection: function () {
                var i, page, models = [];
                // Add first/prev links
                if (options.currentPage > options.startPage) {
                    models.push(new PageModel({
                        text: options.firstLabel,
                        page: options.startPage
                    }));
                    models.push(new PageModel({
                        text: options.prevLabel,
                        page: parseInt(options.currentPage, 10) - 1
                    }));
                }
                // Add numeric links for pages
                for (i = options.startPage; i <= options.totalPages; i++) {
                    models.push(new PageModel({
                        'text': i,
                        'page': i 
                    }));
                }
                // Add next/last links
                if (options.currentPage < options.totalPages) {
                    models.push(new PageModel({
                        text: options.nextLabel,
                        page: parseInt(options.currentPage, 10) + 1
                    }));
                    models.push(new PageModel({
                        text: options.lastLabel,
                        page: options.totalPages
                    }));
                }
                this.collection = new Pages(models);
            },

            initialize: function () {
                this.fillCollection();
                this.render();
            },

            render: function () {
                this.$el = $(document.createElement('ul'));
                this.$el.addClass(options.className);
                this.collection.each(function (item) {
                    this.renderItem(item);
                }, this);
                this.$el.on('click', function (e) {
                    e.preventDefault();
                    if (!_.isUndefined($(e.target).attr('href'))) {
                        options.onChange($(e.target).attr('href'));
                    }
                });
                return this;
            },
            
            renderItem: function (item) {
                var itemView = new Page({
                    model: item
                });
                $(itemView.render().el).appendTo(this.$el);
            }
        });

    return new Paginator();
};
