//
// discussionEntryModel.js
// =======================
// Model to display in list-view.
define(['backbone', 'moment'],

function (Backbone) {
    "use strict";
    
    var DiscussionEntryModel = Backbone.Model.extend({
        initialize: function (params) {
            if (params) {
                this.set('date_created', moment(params.date_created).fromNow());
            }
        }
    });
    
    return DiscussionEntryModel;
});