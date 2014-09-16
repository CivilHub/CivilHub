//
// news-form.js
// ============

require(['jquery',
         'redactor',
         'tagsinput'],

function ($) {
    
    "use strict";
    
    $(document).ready(function () {
        
        $('#id_content').redactor({
            buttons: ['bold', 'italic', 'unorderedlist', 'orderedlist', 'link'],
            plugins: ['uploader']
        });
        
        $('#id_tags').tagsInput({
            autocompleteUrl: '/rest/tags/'
        });
    });
    
});