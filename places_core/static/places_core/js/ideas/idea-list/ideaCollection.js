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
        
        queryParams: {
            totalRecords: 'count'
        },
        
        parse: function (data) {
            return data.results;
        }
    });
    
    return IdeaCollection;
});