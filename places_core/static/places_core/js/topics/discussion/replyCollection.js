//
// replyCollection.js
// ==================
// Paginated collection of all replies.
define(['jquery',
        'underscore',
        'backbone',
        'js/topics/discussion/replyModel'],

function ($, _, Backbone, ReplyModel) {
    "use strict";
    
    var ReplyCollection = Backbone.Collection.extend({
        
        model: ReplyModel,
        
        url: '/rest/replies/',
        
        parse: function (data) {
            
            this.totalResults = data.count;
            
            try {
                this.previousPage = data.previous.slice(data.next.indexOf('page') + 5);
            } catch (e) {
                this.previousPage = null;
            }
            
            try {
                this.nextPage = data.next.slice(data.next.indexOf('page') + 5);
            } catch (e) {
                this.nextPage = null;
            }
            
            return data.results;
        },
        
        getPage: function (page) {
            var self = this;
            page = page || this.nextPage;
            this.fetch({
                data: {
                    pk: self.targetId,
                    page: page
                },
                success: function () {
                    self.currentPage = page;
                }
            });
        }
    });
    
    return ReplyCollection;
});