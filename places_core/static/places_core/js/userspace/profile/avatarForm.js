//
// avatarForm.js
// =============
//
// Change/edit user avatar.
//
require(['jquery',
         'bootstrap',
         'bootstrap-fileinput'],

function ($) {
    "use strict";
    
    var $form = $('#upload-avatar-form'),
        $img = $form.find('#id_avatar');
    
    $img
        .bootstrapFileInput()
        .on('change', function () {
            $form.submit();
        });
});