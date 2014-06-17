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
    
    // Create DOM link element
    // -----------------------
    // Creates links to next and previous result pages.
    var createLink = function (url, text) {
        var a = $(document.createElement('a')),
            url = url || "#";
        a.text(text).attr('href', url)
        if (url !== "#") {
            a.on('click', function (e) {
                e.preventDefault();
                createNewsList(url);
            });
        }
        return a;
    }
    
    // Create paginator
    // ----------------
    // Crates page element with links to all result subpages.
    var createPaginator = function (url, count, perPage) {
        var paginator = $(document.createElement('div')),
            pages = Math.ceil(count / perPage),
            i = 0;
        if (url.indexOf('page') > -1) {
            url = url.slice(0, url.indexOf('page') + 5);
        } else {
            url = url + '&page=';
        }
        for (i = 1; i <= pages; i++) {
            paginator.append(createLink(url + i, i));
        }
        return paginator;
    }
    
    // Create news list
    // ----------------
    var createNewsList = function (url) {
        var next  = '',
            prev  = '',
            paginator = '';
        $('#entries').empty();
        $.get(url, function (resp) {
            paginator = createPaginator(url, resp.count, resp.results.length);
            if (resp.next) {
                next = createLink(resp.next, gettext('Next'));
            }
            if (resp.previous) {
                prev = createLink(resp.previous, gettext('Previous'));
            }
            newsSet = new newsList.ListView(resp.results);
            newsSet.$el.append(prev).append(paginator).append(next);
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