//
// pageable-view.js
// ================
// Klasa do rozszerzenia przez wszystkie widoki korzystające z paginatora.
//
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    // Helper functions
    // ================
    // Funkcja pobierająca dodatkowe dane z formularza 'search'.
    // ---------------------------------------------------------
    var getSearchText = function () {
        var $field = $('#haystack'),
            txt = $field.val();
        
        if (_.isUndefined(txt) || txt.length <= 1) {
            return false;
        }
        
        return txt;
    };
    
    // Wczytanie wybranych opcji.
    // ---------------------------
    // Sprawdzenie aktywnych elementów (klikniętych linków)
    // w celu "pozbierania" opcji wyszukiwarki.
    //
    var getListOptions = function () {
        var $sel = $('.list-controller'),
            opts = {},
            optType = null,
            optValue = null,
            haystack = getSearchText();
        
        $sel.each(function () {
            var $this = $(this);
            
            if ($this.hasClass('active')) {
                optType = $this.attr('data-control');
                optValue = $this.attr('data-target');
                opts[optType] = optValue;
            }
        });
        
        if (haystack !== false) {
            opts['haystack'] = haystack;
        }
        
        return opts;
    };
    
    // PageableView
    // ------------
    var PageableView = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'backbone-collection-list',
        
        template: _.template($('#pageable-view-tpl').html()),
        
        events: {
            'click .first-page': 'firstPage',
            'click .last-page': 'lastPage',
            'click .next-page': 'nextPage',
            'click .prev-page': 'prevPage'
        },
        
        filter: function (page) {
            var self = this,
                filters = getListOptions();

            _.extend(this.collection.queryParams, filters);
            
            this.collection.fetch();
        },
        
        getPage: function (idx) {
            this.collection.getPage(parseInt(idx, 10));
            this.setCounter();
        },
        
        firstPage: function () {
            this.collection.getFirstPage();
            this.setCounter();
        },
        
        lastPage: function () {
            this.collection.getLastPage();
            this.setCounter();
        },
        
        nextPage: function () {
            if (this.collection.hasNextPage()) {
                this.collection.getNextPage();
                this.setCounter();
            }
        },
        
        prevPage: function () {
            if (this.collection.hasPreviousPage()) {
                this.collection.getPreviousPage();
                this.setCounter();
            }
        },
        
        setCounter: function () {
            this.$el.find('.current-page')
                .text(this.collection.state.currentPage);
            this.render();
        }
    });
    
    return PageableView;
});