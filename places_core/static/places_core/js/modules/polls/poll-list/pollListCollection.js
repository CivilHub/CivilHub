//
// pollListCollection.js
// =====================
// Manage all polls belonging to selected location.
define(['backbone', 'paginator'],

function (Backbone) {
    "use strict";
    
    var PollListModel = Backbone.Model.extend({});
    
    var PollListCollection = Backbone.PageableCollection.extend({
        
        model: PollListModel,
        
        url: $('#poll-api-url').val(),
        
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
    
    return PollListCollection;
});