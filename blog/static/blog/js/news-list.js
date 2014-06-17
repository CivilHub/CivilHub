(function ($) {
    "use strict";
    var newsList = {},
        newsSet = null,
        appUrl   = '/rest/news/?pk=' + $('#location-id').val();
    
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
    
    // Create news list
    // ----------------
    var createNewsList = function (url) {
        var pgn  = '';
        $('#entries').empty();
        $.get(url, function (resp) {
            pgn = paginator({
                baseUrl : url,
                total   : resp.count,
                perPage : resp.results.length,
                previous: resp.previous,
                next    : resp.next,
                callback: createNewsList
            });
            newsSet = new newsList.ListView(resp.results);
            newsSet.$el.append(pgn);
        });
    }
    
    // Initialize first results page
    createNewsList(appUrl);
    
    // Enable list sorting.
    $('.news-list-sort-toggle').bind('click', function (e) {
        var order = $(this).attr('data-target'),
            url = appUrl + '&order=' + order;
        e.preventDefault();
        createNewsList(url);
    });
    
    // Enable searching
    $('#news-search-form').bind('submit', function (e) {
        var $qField = $(this).find('#q'),
            keywords = $qField.val(),
            url = appUrl + '&keywords=' + encodeURIComponent(keywords);
        e.preventDefault();
        createNewsList(url);
    });
    
})(jQuery);