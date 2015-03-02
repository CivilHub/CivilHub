//
// subcomment-collection.js
// ========================
// Kolekcja przechowująca odpowiedzi do konkretnego komentarza. Tutaj korzystamy
// ze standardowej kolekcji Backbone, paginacja odpowiedzi nie będzie konieczna.

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