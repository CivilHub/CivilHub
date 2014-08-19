//
// col-view.js
// ============

define(['jquery',
        'underscore',
        'backbone',
        'js/locations/location-list/location-collection',
        'js/locations/location-list/location-list-view'],

function ($, _, Backbone, LocationCollection, LocationListView) {
    
    "use strict";
    
    jQuery.fn.animateAuto = function(prop, speed, callback){
        var elem, height, width;
        return this.each(function(i, el){
            el = jQuery(el), elem = el.clone().css({"height":"auto","width":"auto"}).appendTo("body");
            height = elem.css("height"),
            width = elem.css("width"),
            elem.remove();
            
            if(prop === "height")
                el.animate({"height":height}, speed, callback);
            else if(prop === "width")
                el.animate({"width":width}, speed, callback);  
            else if(prop === "both")
                el.animate({"width":width,"height":height}, speed, callback);
        });  
    }
    
    var ColView = Backbone.View.extend({
        
        tagName: 'ul',
        
        className: 'list-column',
        
        template: _.template($('#list-col-tpl').html()),
        
        events: {
            'click .expand-entry': 'expand',
            'click .close-col': 'destroy'
        },
        
        initialize: function () {
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
            this.$el.appendTo('body');
            if (this.collection.length >= 1) {
                this.$el.html(this.template({})).animateAuto('width', 'fast');
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
            var id = $(e.currentTarget).attr('data-target');
            var pos = {
                top: this.position.top,
                left: this.position.left + this.$el.width()
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
        }
    });
    
    return ColView;
});