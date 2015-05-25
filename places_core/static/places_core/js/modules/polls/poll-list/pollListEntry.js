//
// pollListEntry.js
// ================
// Single poll entry on the list.
define(['jquery',
        'underscore',
        'backbone',
        'moment'],

function ($, _, Backbone) {
    
    "use strict";
    
    var currentLang = window.CivilApp.language || 'en';
    
    var PollListEntry = Backbone.View.extend({
        tagName: 'div',
        
        className: 'polls-list-entry custom-list-entry row',
        
        template: _.template($('#poll-entry').html()),
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            this.$el.find('.date-created')
                .text(moment(this.model.get('date_created'))
                    .lang(currentLang).fromNow());
            if (this.model.get('edited')) {
                this.$el.find('.date-edited')
                    .text(moment(this.model.get('date_edited'))
                        .lang(currentLang).fromNow());
            }
            return this;
        }
    });
    
    return PollListEntry;
});