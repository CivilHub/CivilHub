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
// Wczytanie opcji startowych.
// ---------------------------
// Parsowanie aktywnego url-a w celu ustawienia aktywnych
// elementów w oparciu o wybrane opcje.
//
var loadListOptions = function () {
    var $sel = $('.list-controller'),
        data = urlToJSON(document.location.href);

    if (_.isEmpty(data)) {
        return true;
    }

    $sel.each(function () {
        var key = $(this).attr('data-control'),
            val = $(this).attr('data-target'),
            selected = data[key];
        
        if (val === selected) {
            $(this).addClass('active');
        } else {
            $(this).removeClass('active');
        }
    });
};

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
                var cc = civApp.voteCounter(this.model.get('id'));
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
                that.collection = new IdeaCollection();
                that.collection.fetch({
                    success: function () {
                        that.render();
                    }
                });
            },

            render: function () {
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
            },

            renderEntry: function (item) {
                var itemView = new IdeaView({
                        model: item
                    });
                $(itemView.render().el).appendTo(this.$el);
            },

            filter: function (filters) {
                var that = this;
                that.collection.url = window.IDEA_API_URL + JSONtoUrl(filters);
                console.log(that.collection.url);
                that.collection.fetch({
                    success: function () {
                        that.$el.empty();
                        that.render();
                        console.log(that.collection);
                    }
                });
            }
        });

    return new IdeasList();
};

var ideas = ideaList();

//
// Obsługa kliknięć.
// -----------------
// Po kliknięciu na aktywny link w formularzu ta funkcja
// zbiera wybrane opcje i tworzy URL do przekierowania.
$('.list-controller').bind('click', function (e) {
    var selectedItem = $(this).attr('data-control'),
        options = {},
        url     = '';

    e.preventDefault();

    $('.active[data-control="' + selectedItem + '"]')
        .removeClass('active');
    $(this).addClass('active');

    ideas.filter(getListOptions());
});
$('#haystack-form').bind('submit', function (e) {
    e.preventDefault();
    ideas.filter(getListOptions());
});

})(jQuery);
