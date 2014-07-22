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
    
    var PageEntryView = Backbone.View.extend({
        
        tagName: 'li',
        
        className: 'page-entry',
        
        template: _.template('<a href="#" data-page="<%= page %>"><%= label %></a>'),
        
        initialize: function () {
            this.listenTo(this.model, 'change', this.render);
        },
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
    var PaginatorView = Backbone.View.extend({
        
        tagName: 'ul',
        
        className: 'pagination',
        
        events: {
            'click': 'selectPage'
        },
        
        initialize: function (options) {
            
            var i, page;
            
            this.totalPages = Math.ceil(options.count / options.perPage);
            this.firstPage        = options.startPage || 1;
            this.currentPage      = options.startPage || 1;
            this.collection       = new Backbone.Collection();
            this.targetCollection = options.targetCollection || null;
            this.queryParams      = options.data || {};
            
            this.collection.add([
                new Backbone.Model({page: this.firstPage, label: '<<'}),
                new Backbone.Model({page: this.currentPage - 1, label: gettext("Previous")})
            ]);
            
            for (i = 1; i <= this.totalPages; i++) {
                page = new Backbone.Model({
                    page: i,
                    label: i
                });
                this.collection.add(page);
            }
            
            this.collection.add([
                new Backbone.Model({page: this.currentPage + 1, label: gettext("Next")}),
                new Backbone.Model({page: this.totalPages, label: '>>'})
            ]);
            
            this.linkFirst = this.collection.at(0);
            this.linkPrev  = this.collection.at(1);
            this.linkLast  = this.collection.at(this.collection.length - 1);
            this.linkNext  = this.collection.at(this.collection.length - 2);
        },
        
        render: function () {
            this.collection.each(function (item) {
                this.renderPage(item);
            }, this);
            if (this.totalPages <= 1) {
                this.$el.hide();
            }
            return this;
        },
        
        renderPage: function (item) {
            var page = new PageEntryView({
                model: item
            });
            var $pageEl = $(page.render().el);
            $pageEl.appendTo(this.$el);
            if ($pageEl.find('a:first').attr('data-page') == this.currentPage) {
                $pageEl.addClass('active');
            }
        },
        
        selectPage: function (e) {
            e.preventDefault();
            var page = parseInt($(e.target).attr('data-page'), 10);
            if (!_.isNaN(page)) {
                this.$el.find('li').removeClass('active');
                $(e.target).addClass('active');
                this.setPage(page);
            }
            if (page < this.totalPages) {
                this.linkNext.set('page', page + 1);
            }
            if (page > this.firstPage) {
                this.linkPrev.set('page', page - 1);
            }
            $(document).scrollTop(0);
        },
        
        setPage: function (page) {
            try {
                this.targetCollection.getPage(page, {data: this.queryParams});
                this.currentPage = page;
            } catch (e) {
                console.log(e);
            }
        }
    });
    
    return PaginatorView;
});