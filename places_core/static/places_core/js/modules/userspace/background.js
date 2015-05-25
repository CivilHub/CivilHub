//
// background.js
// =============


require(['jquery',
         'js/modules/ui/image-form'],

function ($) {
    
    "use strict";
    
    $('#user-background-form').hide();
    
    $('#background').on('change', function (e) {
        $('#user-background-form').submit();
    });
    
    $('.change-background-btn').on('click', function (e) {
        $('#background').trigger('click');
    });
    
    $(document).ready(function () {
        var form = new ImageForm({
            $el: $('#user-background-form')
        });
    });
});