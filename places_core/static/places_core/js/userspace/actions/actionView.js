//
// actionView.js
// =============
//
// Single action entry view.
//
define(['underscore', 'backbone'],

function (_, Backbone) {
    "use strict";
    
    var ActionView = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'row action-entry',
        
        template: _.template($('#action-template').html()),
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
    return ActionView;
});