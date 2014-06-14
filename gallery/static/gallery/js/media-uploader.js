(function ($) {
"use strict";
//
// Media uploader core
// -------------------------------------------------------------------------
//
function mediaUploader () {
    var uploader = object('MediaUploader');
    $.extend(uploader, {
        selectedItem: null,

        $el: $('#media-upload-modal'),

        $imgList: {},

        $galList: {},

        dz: {},

        fetchUserGallery: function () {
            $('#user-media-list').empty();
            $.get('/gallery', function (resp) {
                resp = JSON.parse(resp);

                $(resp.files).each(function (idx) {
                    var _this = this,
                        path = resp.href + '/thumbs/' + _this,
                        $img = $(document.createElement('img'));

                    $img.attr({
                        src    : path,
                        'class': 'media-thumbnail'
                    });

                    $('#user-media-list').append($img);

                    $img.on('click', function () {
                        $('.media-uploader-controls').empty().remove();
                        $('.uploader-selected-item')
                            .removeClass('uploader-selected-item');
                        $img.addClass('uploader-selected-item')
                            .after('<span class="media-uploader-controls fa fa-minus-circle"> </span>');
                        $('.media-uploader-controls').on('click', function () {
                            var imgPath = $img.attr('src'),
                                imgName = imgPath.slice(imgPath.lastIndexOf('/') + 1);
                            sendAjaxRequest('DELETE', '/gallery/' + imgName + '/', {
                                success: function (resp) {
                                    display_alert(resp.message, resp.level);
                                    $img.fadeOut('fast', function () {
                                        $img.empty().remove();
                                        $('.media-uploader-controls').empty().remove();
                                    });
                                },
                                error: function (err) {
                                    console.log(err);
                                }
                            });
                        });
                        uploader.selectedItem = resp.href + _this;
                    });
                });
            });
        },

        open: function (callback) {
            this.$el.modal('show');
            this.$el.find('#tabs').tabs();
            if (this.$el.find('#place-media-list').length > 0) {
                uploader.$galList = this.$el.find('#place-media-list');
            }
            // Get items from place gallery.
            // -----------------------------
            if (!_.isEmpty(this.$galList)) {
                var slug = this.$galList.attr('data-target');
                $.get('/' + slug + '/gallery/', function (resp) {
                    resp = JSON.parse(resp);
                    $(resp.files).each(function () {
                        var _this = this,
                            path = resp.href + 'thumbs/' + _this,
                            $img = $(document.createElement('img'));

                        $img.attr({
                            src    : path,
                            'class': 'media-thumbnail'
                        });

                        uploader.$galList.append($img);

                        $img.on('click', function () {
                            $('.media-uploader-controls').empty().remove();
                            $('.uploader-selected-item')
                                .removeClass('uploader-selected-item');
                            $img.addClass('uploader-selected-item');
                            uploader.selectedItem = resp.href + _this;
                        });
                    });
                });
            }
            // Primitive callback to allow fetch picture only once
            // into CKEDITOR instance.
            if (callback) {
                callback();
            }
        },
        
        close: function () {
            this.$el.modal('hide');
        }
    });
    
    uploader.$el.one('shown.bs.modal', function () {
        //
        // Get items from user's gallery directory.
        // -----------------------------------------------------------------
        //
        uploader.fetchUserGallery();
        if (!$('#dropzone-input').hasClass('dropzone')) {
            uploader.dz = new Dropzone('#dropzone-input', {
                init: function () {
                    $('#dropzone-input').addClass('dropzone');
                    this.on("complete", function (file) {
                        if (this.getUploadingFiles().length === 0 &&
                            this.getQueuedFiles().length === 0) {
                            // re-fetch gallery after media upload
                            uploader.fetchUserGallery();
                        }
                    });
                }
            });
        }
    });

    return uploader;
}

$.fn.customCKEditor = function (settings) {
    return $(this).each(function () {
        var $el = $(this),
            editor = CKEDITOR.replace($el.attr('id')),
            uploader = mediaUploader(),
            image = {};
        editor.ui.addButton('MediaUploader', {
            label: gettext('Add Media'),
            command: 'Uploader'
        });
        editor.addCommand('Uploader', {exec: function () {
            uploader.open(function () {
                uploader.$el.find('.submit-btn:first').one('click', function (evt) {
                    image = CKEDITOR.dom.element
                        .createFromHtml( '<img src="' + uploader.selectedItem + '" border="0" />' );
                    editor.insertElement(image);
                    evt.preventDefault();
                    uploader.close();
                });
            });
        }});
        // Load additional CKEDITOR configuration
        for (var key in window.CONFIG.ckeditor[settings]) {
            if (window.CONFIG.ckeditor[settings].hasOwnProperty(key)) {
                editor.config[key] = window.CONFIG.ckeditor[settings][key];
            }
        }
    });
}
})(jQuery);