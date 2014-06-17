(function ($) {
    "use strict";
    var newsList = {},
        appUrl = '/rest/news/?pk=' + $('#location-id').val();
    
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
    
    $.get(appUrl, function (newses) {
        new newsList.ListView(newses);
    });
    
    // Enable list sorting.
    $('.news-list-sort-toggle').bind('click', function (e) {
        var order = $(this).attr('data-target'),
            url = appUrl + '&order=' + order;
        e.preventDefault();
        $('#entries').empty();
        $.get(url, function (newses) {
            new newsList.ListView(newses);
        });
    });
    
    // Enable searching
    $('#news-search-form').bind('submit', function (e) {
        var $qField = $(this).find('#q'),
            keywords = $qField.val(),
            url = appUrl + '&keywords=' + encodeURIComponent(keywords);
        e.preventDefault();
        $('#entries').empty();
        $.get(url, function (newses) {
            new newsList.ListView(newses);
        });
    });
})(jQuery);