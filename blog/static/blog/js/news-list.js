//
// news-list.js
// ============
//
// This is entire blog application.
//
var CivilApp = CivilApp || {};

(function ($) {
"use strict";

var url = CivilApp.BLOG_API_URL;

//
// Funkcja pobierająca dodatkowe dane z formularza 'search'.
// ---------------------------------------------------------
var getSearchText = function () {
    var $field = $('#haystack'),
        txt = $field.val();
    
    if (_.isUndefined(txt) || txt.length <= 1) {
        return '';
    }
    
    return txt;
};
//
// Wczytanie wybranych opcji.
// ---------------------------
// Sprawdzenie aktywnych elementów (klikniętych linków)
// w celu "pozbierania" opcji wyszukiwarki.
// 
var getListOptions = function () {
    var $sel = $('.list-controller'),
        opts = {},
        optType = null,
        optValue = null;
    
    $sel.each(function () {
        var $this = $(this);
        
        if ($this.hasClass('active')) {
            optType = $this.attr('data-control');
            optValue = $this.attr('data-target');
            opts[optType] = optValue;
        }
    });
    
    opts['haystack'] = getSearchText();
    
    return opts;
};
//
// Core function.
// --------------
// Zasadnicza funkcja odpowiedzialna za uruchomienie całego szkieletu
// aplikacji.
//
var newsList = function () {

    var NewsModel = Backbone.Model.extend({}),

        NewsView = Backbone.View.extend({
            tagName: 'div',

            className: 'news-entry',

            template: _.template($('#news-entry-tpl').html()),

            submenu: {},

            events: {
                'click .submenu-toggle': 'openMenu'
            },

            render: function () {
                var that = this;
                this.$el.html(this.template(this.model.toJSON()));
                this.submenu = {
                    $el: that.$el.find('.entry-submenu'),
                    opened: false
                };
                return this;
            },

            openMenu: function () {
                if (this.submenu.opened) {
                    this.submenu.$el.slideUp('fast');
                    this.submenu.opened = false;
                } else {
                    this.submenu.$el.slideDown('fast');
                    this.submenu.opened = true;
                }
            },
        }),

        NewsCollection = Backbone.Collection.extend({
            model: NewsModel,
            url: url
        }),

        NewsList = Backbone.View.extend({
            el: '#entries',

            initialize: function () {
                var that = this;
                $.get(url, function (resp) {
                    resp = JSON.parse(resp);
                    that.collection = new NewsCollection(resp.results);
                    that.render(resp.current_page, resp.total_pages);
                });
            },

            render: function (current_page, total_pages) {
                var that = this;
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
                this.paginator = CivilApp.SimplePaginator({
                    currentPage: current_page,
                    totalPages: total_pages,
                    prevLabel: gettext("Previous"),
                    nextLabel: gettext("Next"),
                    onChange: function (page) {
                        that.filter(page);
                    }
                });
                $(this.paginator.$el).appendTo(this.$el);
            },

            renderEntry: function (item) {
                var itemView = new NewsView({
                        model: item
                    });
                $(itemView.render().el).appendTo(this.$el);
            },

            filter: function (page) {
                var that = this,
                    filters = getListOptions(),
                    url  = CivilApp.BLOG_API_URL + JSONtoUrl(filters);
                if (page) url += '&page=' + page;
                $.get(url, function (resp) {
                    resp = JSON.parse(resp);
                    that.collection = new NewsCollection(resp.results);
                    that.$el.empty();
                    that.render(resp.current_page, resp.total_pages);
                });
            }
        });

    return new NewsList();
};

// Initialize list.
// -----------------------------------------------------------------------------
var blog = newsList();

//
// Obsługa kliknięć.
// -----------------
// Po kliknięciu na aktywny link w formularzu ta funkcja
// zbiera wybrane opcje i tworzy URL do przekierowania.
//
$('.list-controller').bind('click', function (e) {
    var selectedItem = $(this).attr('data-control');

    e.preventDefault();

    $('.active[data-control="' + selectedItem + '"]')
        .removeClass('active');
    $(this).addClass('active');

    blog.filter();
});
//
// Zapisanie formularza.
// ---------------------
// W taki sam sposób jak powyżej, łączymy submit formularza.
//
$('#haystack-form').bind('submit', function (e) {
    e.preventDefault();
    blog.filter();
});

})(jQuery);
