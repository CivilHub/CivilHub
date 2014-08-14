//
// ideaCollection.js
// =================
// Manage list of ideas.
define(['backbone',
        'js/ideas/idea-list/ideaModel',
        'paginator'],

function (Backbone, IdeaModel) {
    "use strict";
    
    var IdeaCollection = Backbone.PageableCollection.extend({
        
        model: IdeaModel,
        
        url: $('#rest-api-url').val(),
        
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
    
    return IdeaCollection;
});