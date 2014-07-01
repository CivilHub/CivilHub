//
// simple-paginator.js
// ===================
//
// Paginacja wyników zapytań do widoków typu REST nie powiązanych z Django
// REST Framework (tzn. korzystających bezpośrednio z widoków Django).
// Ponieważ chcemy przesyłać wyniki w nieco innej formie, nie możemy tutaj
// skorzystać z rest-paginator.js.
//
var CivilApp = CivilApp || {};

CivilApp.SimplePaginator = function (options) {
    
    var defaults = {
            startPage  : 1,
            currentPage: 1,
            totalPages : 10,
            className  : 'pagination',
            activeClass: 'active',
            onChange: function (page) {
                console.log(page);
            }
        },
    
        options = $.extend(defaults, options),
        
        PageModel = Backbone.Model.extend({}),
        
        Page = Backbone.View.extend({
            tagName: 'li',
            
            template: _.template('<a href="<%= page %>"><%= text %></a>'),
            
            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                if (this.model.get('page') === options.startPage)
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
                for (i = options.startPage; i <= options.totalPages; i++) {
                    models.push(new PageModel({
                        'text': i,
                        'page': i 
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
