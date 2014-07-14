//
// ideaCollection.js
// =================
// Manage list of ideas.
define(['backbone',
        'js/ideas/idea-list/ideaModel'],

function (Backbone, IdeaModel) {
    "use strict";
    
    var IdeaCollection = Backbone.Collection.extend({
        model: IdeaModel
    });
    
    return IdeaCollection;
});