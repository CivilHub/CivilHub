//
// background.js
// =============
//
require(['jquery'],

function ($) {
    
    "use strict";
    
    $('#user-background-form').hide();
    
    $('#background').on('change', function (e) {
        $('#user-background-form').submit();
    });
    
    $('.change-background-btn').on('click', function (e) {
        $('#background').trigger('click');
    });
});