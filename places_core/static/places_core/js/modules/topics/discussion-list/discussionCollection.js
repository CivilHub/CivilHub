//
// discussionCollection.js
// =======================
// Manage entire location's forum list.
define(['backbone',
        'js/modules/topics/discussion-list/discussionEntryModel',
        'paginator'],

function (Backbone, DiscussionEntryModel) {
    
    "use strict";
    
    var DiscussionCollection = Backbone.PageableCollection.extend({
        
        model: DiscussionEntryModel,
        
        url: $('#discussion-api-url').val(),
        
        mode: 'server',
        
        queryParams: {
            totalRecords: 'count'
        },
        
        parseRecords: function (data) {
            return data.results;
        },
        
        parseState: function (resp, queryParams, state, options) {
            return {totalRecords: resp.count};
        }
    });
    
    return DiscussionCollection;
});