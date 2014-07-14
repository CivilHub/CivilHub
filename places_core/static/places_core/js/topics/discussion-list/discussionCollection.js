//
// discussionCollection.js
// =======================
// Manage entire location's forum list.
define(['backbone',
        'js/topics/discussion-list/discussionEntryModel'],

function (Backbone, DiscussionEntryModel) {
    "use strict";
    
    var DiscussionCollection = Backbone.Collection.extend({
        model: DiscussionEntryModel
    });
    
    return DiscussionCollection;
});