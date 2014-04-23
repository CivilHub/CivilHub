(function ($) {
    "use strict";
    var $form = $('#pl-register-form'),
        $pass = $('#password'),
        $chk  = $('#passchk');
    $chk.on('keyup', function () {
        if ($pass.val() === $chk.val()) {
            $pass.css('border', '1px solid green');
        }
    });
})(jQuery);
