//
// pageable-view.js
// ================
// Klasa do rozszerzenia przez wszystkie widoki korzystające z paginatora.
//
define(['jquery',
        'underscore',
        'backbone',
        'utils'],

function ($, _, Backbone, utils) {
    
    "use strict";
    
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
                filters = utils.getListOptions();

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