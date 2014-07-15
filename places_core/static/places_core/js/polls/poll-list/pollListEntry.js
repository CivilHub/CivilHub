//
// pollListEntry.js
// ================
// Single poll entry on the list.
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    
    "use strict";
    
    var PollListEntry = Backbone.View.extend({
        tagName: 'div',
        
        className: 'polls-list-entry custom-list-entry row',
        
        template: _.template($('#poll-entry').html()),
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
    return PollListEntry;
});