//
// discussion-list.js
// ==================
//
// Lista tematów na forum.
//
var CivilApp = CivilApp || {};

//
// Main application
// -----------------------------------------------------------------------------
//
CivilApp.DiscussionList = function () {
    
    var url = CivilApp.TOPIC_API_URL,
    
        Model = Backbone.Model.extend({}),
        
        View = Backbone.View.extend({
            tagName: 'div',
            className: 'topic-list-entry custom-list-entry',
            template: _.template($('#topic-entry').html()),
            
            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                return this;
            }
        }),
        
        Collection = Backbone.Collection.extend({
            model: Model
        }),
        
        List = Backbone.View.extend({
            el: '#discussions',
            
            _init: function (data) {
                var that = this;
                data = JSON.parse(data);
                this.collection = new Collection(data.results);
                this.paginator = CivilApp.SimplePaginator({
                    currentPage: data.current_page,
                    totalPages: data.total_pages,
                    onChange: function (page) {
                        that.filter(page);
                    }
                });
                this.$el.empty();
                this.render();
            },
            
            initialize: function () {
                var that = this;
                $.get(CivilApp.TOPIC_API_URL, function (resp) {
                    that._init(resp);
                });
            },
            
            render: function () {
                this.collection.each(function (item) {
                    this.renderItem(item);
                }, this);
                this.paginator.$el.appendTo(this.$el);
            },
            
            renderItem: function (item) {
                var view = new View({model:item});
                $(view.render().el).appendTo(this.$el);
            },
            
            filter: function (page) {
                var that = this,
                    filters = getListOptions(),
                    url  = CivilApp.TOPIC_API_URL + JSONtoUrl(filters);
                if (page) url += '&page=' + page;
                $.get(url, function (resp) {
                    that._init(resp);
                });
            }
        });
        
    return new List();
};

//
// Run scripts
// -----------------------------------------------------------------------------
//
(function ($, f) {
"use strict";

var app = f.DiscussionList();
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

    app.filter();
});
//
// Zapisanie formularza.
// ---------------------
// W taki sam sposób jak powyżej, łączymy submit formularza.
//
$('#haystack-form').bind('submit', function (e) {
    e.preventDefault();
    app.filter();
});

})(jQuery, CivilApp);
