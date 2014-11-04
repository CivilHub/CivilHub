//
// background.js
// =============
//
require(['jquery',
         'fileinput'],

function ($) {
    
    "use strict";
    
    $(document).ready(function () {

        $('#id_image').on('change', function (e) {
            $('#location-background-form').submit();
        });
        
        $('.change-background-btn').on('click', function (e) {
            $('#id_image').trigger('click');
        });
    });
});