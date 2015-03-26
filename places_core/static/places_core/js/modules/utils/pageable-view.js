//
// pageable-view.js
// ================
// A class to broaden by all list views that make use of paginators, i. e.
// a list of discussions, polls, blog section and the idea section.

define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    // Helper functions
    // ================
    // This function downloads additional data from the 'search' form
    // ---------------------------------------------------------
    var getSearchText = function () {
        var $field = $('#haystack'),
            txt = $field.val();
        
        if (_.isUndefined(txt) || txt.length <= 1) {
            return false;
        }
        
        return txt;
    };
    
    // Load selected options.
    // ---------------------------
    // Check the selected elements (clicked links)
    // in order to "gather" search options
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
        
        filter: function (options) {
            var filters = options || getListOptions();
            _.extend(this.collection.queryParams, filters);
            this.filtered = true;
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