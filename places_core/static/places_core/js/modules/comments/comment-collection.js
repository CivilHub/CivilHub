//
// comment-collection.js
// =====================
// Paginowalna kolekcja dla głównej listy komentarzy. Wczytywanie strony odbywa
// się w tzw. infinite mode, tzn. każda nowa strona dodawana jest do kolekcji.

define(['jquery',
        'underscore',
        'backbone',
        'js/modules/comments/comment-model',
        'paginator'],

function ($, _, Backbone, CommentModel) {
    
    "use strict";
    
    var CommentCollection = Backbone.PageableCollection.extend({
        
        model: CommentModel,
        
        mode: 'server',
        
        url: '/rest/comments/',
        
        queryParams: {
            totalRecords: 'count',
            'content-label': $('#target-label').val(),
            'content-type': $('#target-type').val(),
            'content-id': $('#target-id').val()
        },
        
        parseRecords: function (data) {
            return data.results;
        },
        
        parseState: function (resp, queryParams, state, options) {
            return {totalRecords: resp.count};
        }
    });
    
    return CommentCollection;
});