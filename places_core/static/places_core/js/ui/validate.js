//
// validate.js
// ===========
// Simple validation for registration form.
//
require(['jquery', 'bootstrap'], function ($) {
    "use strict";
    
    $.fn.validateRegisterForm = function () {
        
        return $(this).each(function () {
            
            var $form = $(this);

            $form.find('input').each(function () {
                var $input = $(this);
                if (!$input.val()) {
                    $input.popover({
                        content: gettext("This field cannot be empty!")
                    });
                    $input.popover('show');
                    return false;
                }
            });
        });
    };
});