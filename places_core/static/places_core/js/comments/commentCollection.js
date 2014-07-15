//
// commentCollection.js
// ====================
// Manages comments list.
define(['backbone',
        'js/comments/commentModel'],

function (Backbone, CommentModel) {
    "use strict";
    
    var CommentCollection = Backbone.Collection.extend({
        model: CommentModel
    });
    
    return CommentCollection;
});