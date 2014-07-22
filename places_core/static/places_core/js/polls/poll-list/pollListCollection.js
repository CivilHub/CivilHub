//
// pollListCollection.js
// =====================
// Manage all polls belonging to selected location.
define(['backbone', 'paginator', 'moment'],

function (Backbone) {
    "use strict";
    
    var PollListModel = Backbone.Model.extend({
        initialize: function (params) {
            if (params) {
                this.set('date_created', moment(params.date_created).fromNow());
            }
        }
    });
    
    var PollListCollection = Backbone.PageableCollection.extend({
        
        model: PollListModel,
        
        url: $('#poll-api-url').val(),
        
        parse: function (data) {
            return data.results;
        }
    });
    
    return PollListCollection;
});