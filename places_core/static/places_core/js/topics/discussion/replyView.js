//
// replyView.js
// ============
// Single reply.
define(['jquery',
        'underscore',
        'backbone'],

function ($, _, Backbone) {
    "use strict";
    
    var ReplyView = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'reply-entry',
        
        template: _.template($('#reply-tpl').html()),
        
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
    return ReplyView;
});