//
// profileForm.js
// ==============
//
// Edit user's profile.
//
require(['jquery',
         'jqueryui'],

function ($) {
    "use strict";
    
    $('#birth-date').datepicker({
        changeMonth: true,
        changeYear: true,
        minDate: new Date(1920, 1 - 1, 1),
        maxDate: 0,
        dateFormat: 'dd/mm/yy'
    });
    
    //$('#id_description').customCKEditor('custom');
});