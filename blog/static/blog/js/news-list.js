(function ($) {
    "use strict";
    var newsList = {};
    
    newsList.News = Backbone.Model.extend({});
    
    newsList.NewsView = Backbone.View.extend({
        tagName: 'div',
        className: 'news-entry',
        template: _.template($('#news-entry-tpl').html()),
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
    newsList.ListView = Backbone.View.extend({
        el: '#entries',
        
        initialize: function (initialNews) {
            this.collection = new newsList.NewsList(initialNews);
            this.render();
        },
        
        render: function () {
            this.collection.each(function (item) {
                this.renderNews(item);
            }, this);
        },
        
        renderNews: function (item) {
            var NewsView = new newsList.NewsView({
                model: item
            });
            $(NewsView.render().el).appendTo(this.$el);
        }
    });
    
    newsList.NewsList = Backbone.Collection.extend({
        model: newsList.News
    });
    
    $.get('/rest/news/', function (newses) {
        new newsList.ListView(newses);
    });
})(jQuery);