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
        
        className: 'list-column col-sm-3',
        
        template: _.template($('#list-col-tpl').html()),
        
        events: {
            'click .expand-entry': 'expand',
            'click .close-col': 'destroy'
        },
        
        items: {}, // Placeholder dla viewsów powiązanych z modelami kolekcji.
        
        initialize: function () {
            // TODO: przechwytywanie błędów w przypadku podania złych argumentów.
            this.locationID = arguments[1];
            this.tier = arguments[2];
            this.collection = new LocationCollection();
            this.collection.url = 
                '/api-locations/sublocations/?pk=' + this.locationID;
            this.collection.fetch();
            this.listenTo(this.collection, 'sync', this.render);
        },
        
        render: function () {
            var self = this;
            this.$el.appendTo('#list-placeholder > .placeholder-content');
            if (this.collection.length >= 1) {
                this.$el.html(this.template({tier: this.tier}));
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
            }
            this.$el.addClass('tab-offset-' + this.tier);
            this.$el.find('.search-entry').on('keyup', function (e) {
                self.filter($(this).val());
            });
        },
        
        renderEntry: function (item) {
            var entry = new LocationListView({
                model: item
            });
            var $el = $(entry.render().el);
            entry.parentView = this;
            this.items[item.get('id')] = entry;
            $el.appendTo(this.$el);
        },
        
        filter: function (s) {
            var re = new RegExp(s, 'i');
            var model = null;
            _.each(this.items, function (item, idx) {
                model = this.collection.get(idx);
                // FIXME: kolekcje kilku widoków zdają się łączyć w jedną, co
                // skutkuje sprawdzaniem nieistniejących indexów elementów.
                if (model === undefined) return false;
                if (!re.test(model.get('name'))) {
                    item.hide();
                } else {
                    item.show();
                }
            }, this);
        },
        
        expand: function (e) {
            e.preventDefault();
            // Jeżeli lista sub-lokacji jest już otwarta, nie otwieramy nowej.
            if (this.sublist !== undefined) {
                return false;
            }
            var id = $(e.currentTarget).attr('data-target');
            this.items[id].details();
            this.$el.scrollTop(0); // Hack dla google-chrome
            this.sublist = new ColView([], id, this.tier + 1);
            this.listenTo(this.sublist.collection, 'sync', function () {
                // Sprawdzamy, czy ten element ma jakieś inne zagnieżdżone
                // lokacje. Jeżeli nie, kasujemy listę. Podobnie postępujemy
                // w przypadku ostatniego zagnieżdżenia.
                if (!this.sublist.collection.length > 0 || this.tier >= 3) {
                    this.sublist.$el.empty().remove();
                    delete this.sublist;
                    this.$el.addClass('is-last-entry');
                } else {
                    this.sublist.parentView = this;
                    this.$el.removeClass('is-last-entry');
                }
            });
        },
        
        cleanDetails: function () {
            _.each(this.items, function (item, index) {
                if (this.collection.get(index) !== undefined) {
                    item.hideDetails();
                }
            }, this);
        },
        
        destroy: function () {
            this.$el.fadeOut('fast', function () {
                this.$el.empty().remove();
            }.bind(this));
            if (this.sublist !== undefined) {
                this.sublist.destroy();
            }
            if (this.parentView != undefined) {
                // Sublista - usuń ją z indexu nadrzędnej
                delete this.parentView.sublist;
                // Ukryj detale poprzednich elementów
                this.parentView.cleanDetails();
            } else {
                // Pierwsza, podstawowa lista. Emitujemy sygnał i zamykamy
                // okno z przeglądarką lokalizacji.
                this.trigger('destroyed');
            }
        }
    });
    
    return ColView;
});