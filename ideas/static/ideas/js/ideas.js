//
// Handle ideas list for single location.
// ======================================
//
(function ($) {
"use strict";

var url = window.IDEA_API_URL;

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
var ideaList = function () {

    var IdeaModel = Backbone.Model.extend({}),

        IdeaView = Backbone.View.extend({
            tagName: 'div',

            className: 'row idea-entry',

            template: _.template($('#idea-entry-tpl').html()),

            submenu: {},

            events: {
                'click .submenu-toggle': 'openMenu',
                'click .idea-vote-count': 'voteCounterWindow'
            },

            render: function () {
                var that = this;
                this.$el.html(this.template(this.model.toJSON()));
                this.submenu = {
                    $el: that.$el.find('.entry-submenu'),
                    opened: false
                };
                this.$el.find('.vote-btn').tooltip({
                    placement: 'right'
                });
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

            voteCounterWindow: function () {
                var cc = CivilApp.voteCounter(this.model.get('id'));
            }
        }),

        IdeaCollection = Backbone.Collection.extend({
            model: IdeaModel,
            url: url
        }),

        IdeasList = Backbone.View.extend({
            el: '#idea-list-view',

            initialize: function () {
                var that = this;
                $.get(url, function (resp) {
                    resp = JSON.parse(resp);
                    that.collection = new IdeaCollection(resp.results);
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
                    onChange: function (page) {
                        that.filter(page);
                    }
                });
                $(this.paginator.$el).appendTo(this.$el);
            },

            renderEntry: function (item) {
                var itemView = new IdeaView({
                        model: item
                    });
                $(itemView.render().el).appendTo(this.$el);
            },

            filter: function (page) {
                var that = this,
                    filters = getListOptions(),
                    url  = window.IDEA_API_URL + JSONtoUrl(filters);
                if (page) url += '&page=' + page;
                $.get(url, function (resp) {
                    resp = JSON.parse(resp);
                    that.collection = new IdeaCollection(resp.results);
                    that.$el.empty();
                    that.render(resp.current_page, resp.total_pages);
                });
            }
        });

    return new IdeasList();
};

// Initialize idea list.
// -----------------------------------------------------------------------------
var ideas = ideaList();

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

    ideas.filter();
});
//
// Zapisanie formularza.
// ---------------------
// W taki sam sposób jak powyżej, łączymy submit formularza.
//
$('#haystack-form').bind('submit', function (e) {
    e.preventDefault();
    ideas.filter();
});

})(jQuery);
