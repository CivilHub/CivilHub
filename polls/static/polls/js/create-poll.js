(function ($) {
    "use strict";
    var editor = CKEDITOR.replace('id_description');
    $('#id_tags').tagsInput({
        autocomplete_url: '/rest/tags/',
    });
})(jQuery);