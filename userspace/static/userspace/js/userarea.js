(function ($) {
    "use strict";
    $('#id_avatar').bootstrapFileInput();
    $('#birth-date').datepicker({
        changeMonth: true,
        changeYear: true,
        maxDate: 0
    });
    $('#id_avatar').on('change', function () {
        $('#upload-avatar-form').submit();
    });
})(jQuery);