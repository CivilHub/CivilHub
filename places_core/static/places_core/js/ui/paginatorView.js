//
// paginatorView.js
// ================
// Simple Backbone view to display navigation for PageableCollection.
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
        
        events: {
            'click .first-page': 'firstPage',
            'click .last-page': 'lastPage',
            'click .next-page': 'nextPage',
            'click .prev-page': 'prevPage'
        },
        
        initialize: function (collection) {
            this.collection = collection;
        },
        
        render: function () {
            var self = this;
            this.$el.html(this.template(this.collection.state));
            this.$el.find('.page').on('click', function (e) {
                self.getPage($(this).attr('data-index'));
            });
            return this;
        },
        
        getPage: function (idx) {
            this.collection.getPage(parseInt(idx, 10));
        },
        
        firstPage: function () {
            this.collection.getFirstPage();
        },
        
        lastPage: function () {
            this.collection.getLastPage();
        },
        
        nextPage: function () {
            if (this.collection.hasNextPage()) {
                this.collection.getNextPage();
            }
        },
        
        prevPage: function () {
            if (this.collection.hasPreviousPage()) {
                this.collection.getPreviousPage();
            }
        }
    });
    
    return PaginatorView;
});