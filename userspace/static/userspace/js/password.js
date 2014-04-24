(function ($) {
    "use strict";
    var $form = $('form:first'),
        $pass = $('#password'),
        $chk  = $('#passchk');
    $chk.on('keyup', function () {
        if ($pass.val() === $chk.val()) {
            $pass.css('border', '1px solid green');
        }
    });
    $form.on('submit', function () {
        if ($pass.val() === '' || $chk.val() === '') {
            bootbox.alert("Password can't be empty!");
        } else if ($pass.val() !== $chk.val()) {
            bootbox.alert('Passwords not match!');
        } else {
            return true;
        }
        return false;
    });
})(jQuery);
