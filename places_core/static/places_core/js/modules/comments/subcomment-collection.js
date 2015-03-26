//
// subcomment-collection.js
// ========================

// A collection that stores the answers to a given comment. Here we make use
// of the standard Backbone collection, pagination of answers will not be necessary.


define(['jquery',
        'underscore',
        'backbone',
        'js/modules/comments/comment-model'],

function ($, _, Backbone, CommentModel) {
    
    "use strict";
    
    var SubcommentCollection = Backbone.Collection.extend({
        
        model: CommentModel
    });
    
    return SubcommentCollection;
});