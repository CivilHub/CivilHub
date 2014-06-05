(function ($) {
    "use strict";
    $('#id_avatar').bootstrapFileInput();
    $('#birth-date').datepicker({
        changeMonth: true,
        changeYear: true,
        minDate: new Date(1920, 1 - 1, 1),
        maxDate: 0
    });
    $('#id_description').customCKEditor();
    $('#id_avatar').on('change', function () {
        $('#upload-avatar-form').submit();
    });
    $('.user-badge-thumb').tooltip();
})(jQuery);