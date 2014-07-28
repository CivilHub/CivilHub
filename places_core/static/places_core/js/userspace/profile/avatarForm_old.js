//
// avatarForm.js
// =============
//
// Change/edit user avatar.
//
require(['jquery',
         'bootstrap'],

function ($) {
    "use strict";
    
    var $form = $('#upload-avatar-form'),
        $img = $form.find('#id_avatar');
    
    $img
        .on('change', function () {
            $form.submit();
        });
});