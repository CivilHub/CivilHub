//
// replyCollection.js
// ==================
// Paginated collection of all replies.
define(['jquery',
        'underscore',
        'backbone',
        'js/modules/topics/discussion/replyModel',
        'paginator'],

function ($, _, Backbone, ReplyModel) {
    "use strict";
    
    var ReplyCollection = Backbone.PageableCollection.extend({
        
        model: ReplyModel,
        
        url: '/rest/replies/',
        
        counter: 0,
        
        parse: function (data) {
            // Allow to get total count from other viewses:
            this.totalResultsCounter = data.count;
            return data.results;
        },
    });
    
    return ReplyCollection;
});