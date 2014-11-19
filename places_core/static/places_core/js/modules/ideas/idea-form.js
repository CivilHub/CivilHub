//
// idea-form.js
// ============
//
// Formularz dodawania nowego pomysłu - skrypt inicjalizacyjny.
// -----------------------------------------------------------------------------

require(['jquery',
         'redactor',
         'js/modules/ui/mapinput',
         'tagsinput'],

function ($) {
    
    "use strict";
    
    $(document).ready(function () {
        
        $('#id_description').redactor({
            buttons: ['bold', 'italic', 'unorderedlist', 'orderedlist', 'link'],
            plugins: ['uploader']
        });
        
        $('#id_tags').tagsInput({
            autocomplete_url: '/rest/tags/',
            defaultText: gettext("Add tag")
        });
        
        $('#id_latitude, #id_longitude')
            .css('display', 'none');
        
        $('<div id="map"></div>')
            .insertAfter('#id_longitude')
            .mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 640,
                height: 480
            });
    });
    
});