//
// customCKEditor.js
// =================
//
// Custom CKEditor plugin.
//
define(['jquery',
        'ckeditor',
        'js/editor/config',
        'js/editor/mediaUploader'],

function ($, CKEDITOR, config, mediaUploader) {
    "use strict";
    
    $.fn.customCKEditor = function (settings) {
        return $(this).each(function () {
            var $el = $(this),
                editor = CKEDITOR.replace($el.attr('id')),
                uploader = null,
                image = {};
            editor.ui.addButton('MediaUploader', {
                label: gettext('Add Media'),
                command: 'Uploader'
            });
            editor.addCommand('Uploader', {exec: function () {
                uploader = mediaUploader({
                    callback: function (item) {
                        if (!_.isNull(item)) {
                            image = CKEDITOR.dom.element
                                .createFromHtml( '<img src="' + item + '" border="0" />' );
                            editor.insertElement(image);
                        }
                    }
                });
            }});
            // Load additional CKEDITOR configuration
            for (var key in config[settings]) {
                if (config[settings].hasOwnProperty(key)) {
                    editor.config[key] = config[settings][key];
                }
            }
            // Give API endpoint to manipulate editor instance.
            $el.data('editor', editor);
        });
    };
});