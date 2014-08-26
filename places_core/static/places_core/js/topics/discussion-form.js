//
// discussion-form.js
// ==================
//
// Formularz do tworzenia/edycji dyskusji
//
//  => /templates/locations/location_forum_create.html
//
// -----------------------------------------------------------------------------

require(['jquery',
         'mapinput',
         'bootstrap-switch'],

function ($) {
    
    "use strict";
    
    $(document).ready(function () {
        
        $('#id_tags').tagsInput({
            autocomplete_url: '/rest/tags/'
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
        
        $('[type="checkbox"]').bootstrapSwitch({
            onText: gettext("Opened"),
            offText: gettext("Closed"),
            wrapperClass: 'form-group',
            onColor: 'success',
            offColor: 'danger'
        });
    });
});