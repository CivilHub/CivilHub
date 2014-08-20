//
// col-view.js
// ============
// Widok pojedynczej kolumny powiązanej z jednym konkretnym miejscem. Tutaj
// pokazujemy listę wszystkich lokalizacji "dziedziczących" z poprzednio wy-
// branej (lub z wybranego kraju, jeżeli jest to pierwsza kolumna).

define(['jquery',
        'underscore',
        'backbone',
        'js/locations/location-list/location-collection',
        'js/locations/location-list/location-list-view'],

function ($, _, Backbone, LocationCollection, LocationListView) {
    
    "use strict";
    
    var ColView = Backbone.View.extend({
        
        tagName: 'ul',
        
        className: 'list-column',
        
        template: _.template($('#list-col-tpl').html()),
        
        events: {
            'click .expand-entry': 'expand',
            'click .close-col': 'destroy'
        },
        
        initialize: function () {
            // TODO: przechwytywanie błędów w przypadku podania złych argumentów.
            this.locationID = arguments[1];
            this.position = arguments[2];
            this.collection = new LocationCollection();
            this.collection.url = 
                '/api-locations/sublocations/?pk=' + this.locationID;
            this.collection.fetch();
            this.listenTo(this.collection, 'sync', this.render);
        },
        
        render: function () {
            var self = this;
            this.$el.appendTo('body').css('display', 'none');
            if (this.collection.length >= 1) {
                this.$el.html(this.template({})).slideDown('fast');
                this.$el.css({
                    left: self.position.left,
                    top: self.position.top
                });
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
            }
        },
        
        renderEntry: function (item) {
            var entry = new LocationListView({
                model: item
            });
            $(entry.render().el).appendTo(this.$el);
        },
        
        expand: function (e) {
            e.preventDefault();
            if (this.sublist !== undefined) {
                return false;
            }
            var id = $(e.currentTarget).attr('data-target');
            var pos = {
                top: this.position.top,
                left: this.position.left + this.$el.width() + 20
            };
            this.sublist = new ColView([], id, pos);
            this.sublist.parentView = this;
        },
        
        destroy: function () {
            this.$el.fadeOut('fast', function () {
                this.$el.empty().remove();
            }.bind(this));
            if (this.sublist !== undefined) {
                this.sublist.destroy();
            }
            if (this.parentView != undefined) {
                delete this.parentView.sublist;
            } else {
                delete window.activeSublist;
            }
        }
    });
    
    return ColView;
});