//
// sublocations-popover.js
// =======================
//
// Skrypty odpowiadające za wyświetlanie/filtrowanie menu sub-lokalizacji
// w pasku nawigacji w widoku lokalizacji.
//
// Fixme - dropdown z BS nie działa dokładnie w ten sam sposób - tworzony dyna-
// micznie element nie ma dowiązanych eventów, które np. zamkną okienko. Dlatego
// tutaj nie zajmujemy się zamykaniem okna - robimy to w skrypcie, który wywołuje
// kolekcję (e.g. common.js).
//

define(['jquery',
        'underscore',
        'backbone',
        'bootstrap'],

function ($, _, Backbone) {
    
    "use strict";
    
    var ListEntryModel = Backbone.Model.extend({
        defaults: {'id': 0,'name': 'Unknown','slug': 'unknown'}
    });
    
    var ListEntryView = Backbone.View.extend({
        
        tagName: 'li',
        
        className: 'sublocation-list-entry',
        
        template: _.template('<a href="/<%= slug %>/"><%= name %></a>'),
        
        events: {
            'click a': 'redirect'
        },
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        
        redirect: function () {
            document.location.href = '/' + this.model.get('slug') + '/';
        }
    });
    
    var ListEntryCollection = Backbone.Collection.extend({
        model: ListEntryModel
    });
    
    var ListView = Backbone.View.extend({
        
        tagName: 'ul',
        
        className: 'dropdown-menu ancestors-menu',
        
        template: _.template($('#ancestors-menu-tpl').html()),
        
        entries: {}, // Match models with views in collection by model ID
        
        events: {
            'click .fa-search': 'toggleSearch'
        },
        
        initialize: function (opts) {
            this.toggle = opts.toggle;
            $.get('/api-locations/sublocations/?pk='+opts.id,
                function (response) {
                    this.collection = new ListEntryCollection(response);
                    this.render();
                }.bind(this)
            );
        },
        
        render: function () {
            this.$el.html(this.template({}))
                .appendTo(this.toggle)
                .dropdown('toggle');
                
            this.collection.each(function (item) {
                this.renderEntry(item);
            }, this);
            
            this.$el.find('input').on('keyup', function (e) {
                this.filter($(e.currentTarget).val());
            }.bind(this));
        },
        
        renderEntry: function (item) {
            var entry = new ListEntryView({model:item});
            var $el = $(entry.render().el);
            $el.appendTo(this.$el);
            this.entries[item.id] = $el;
        },
        
        filter: function (search) {
            var re = new RegExp(search, 'i'),
                model = null;
            this.collection.each(function (item) {
                if (re.test(item.get('name'))) {
                    this.entries[item.get('id')].show();
                } else {
                    this.entries[item.get('id')].hide();
                }
            }, this);
        },
        
        toggleSearch: function () {
            this.$el.find('.search-title').toggle();
        },
        
        destroy: function () {
            this.collection = null;
            this.$el.off();
            this.$el.empty().remove();
        }
    });
    
    return ListView;
});
