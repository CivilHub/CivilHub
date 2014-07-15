//
// pollListCollection.js
// =====================
// Manage all polls belonging to selected location.
define(['backbone'],

function (Backbone) {
    "use strict";
    
    var PollListModel = Backbone.Model.extend({});
    
    var PollListCollection = Backbone.Collection.extend({
        model: PollListModel
    });
    
    return PollListCollection;
});