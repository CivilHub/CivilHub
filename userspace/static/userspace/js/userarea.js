(function ($) {
    "use strict";
    $('#id_avatar').bootstrapFileInput();
    $('#id_avatar').on('change', function () {
        $('#upload-avatar-form').submit();
    });
})(jQuery);