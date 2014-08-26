//
// idea-form.js
// ============
//
// Formularz dodawania nowego pomysłu - skrypt inicjalizacyjny.
// -----------------------------------------------------------------------------

require(['jquery',
         'redactor',
         'tagsinput'],

function ($) {
    
    "use strict";
    
    $(document).ready(function () {
        
        $('#id_description').redactor({
            plugins: ['uploader']
        });
        
        $('#id_tags').tagsInput({
            autocompleteUrl: '/rest/tags/'
        });
    });
    
});