//
// discussionCollection.js
// =======================
// Manage entire location's forum list.
define(['backbone',
        'js/topics/discussion-list/discussionEntryModel',
        'paginator'],

function (Backbone, DiscussionEntryModel) {
    "use strict";
    
    var DiscussionCollection = Backbone.PageableCollection.extend({
        
        model: DiscussionEntryModel,
        
        url: $('#discussion-api-url').val(),
        
        parse: function (data) {
            return data.results;
        }
    });
    
    return DiscussionCollection;
});