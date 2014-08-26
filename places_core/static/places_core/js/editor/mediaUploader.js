//
// mediaUploader.js
// ================
//
// Media uploader plugin for Redactor.
//

define(['jquery', 'dropzone', 'utils', 'jqueryui'],

function ($, Dropzone, utils) {
    
    "use strict";
    
    var USER_GALLERY_URL = '/rest/usermedia/';
    
    var PLACE_GALLERY_URL = '/rest/gallery/';

    Dropzone.autoDiscover = false;

    var fetchGallery = function (callback) {
            $.get(USER_GALLERY_URL, function (resp) {
                if (typeof(callback) === 'function') {
                    callback(resp);
                }
            });
        },

        createDropzone = function () {
            var $dz = $('#dropzone-input');
            if ($dz.data('dropzone') !== undefined) {
                // If dropzone already exists, 
                // their is no need to create new one.
                return $dz.data('dropzone');
            } else {
                return new Dropzone('#dropzone-input', {
                    init: function () {
                        var that = this;
                        that.on("complete", function (file) {
                            if (that.getUploadingFiles().length === 0 &&
                                that.getQueuedFiles().length === 0) {
                                // re-fetch gallery after media upload
                                //uploader.fetchUserGallery();
                                $('#media-upload-modal')
                                    .data('mediaUploader')
                                    .refetch();
                            }
                        });
                        // Add dropzone to element's data to avoid 'Dropzone
                        // already attached' error.
                        $('#dropzone-input')
                            .addClass('dropzone')
                            .data('dropzone', that);
                    }
                });
            }
        },

        MediaItemModel = Backbone.Model.extend({}),

        MediaItemView = Backbone.View.extend({
            tagName:   'div',

            className: 'media-entry',

            template:  _.template($('#media-item-tpl').html()),

            events: {
                'click .delete-item-button': 'removeItem'
            },

            render: function () {
                this.$el.html(this.template(this.model.toJSON()));
                return this;
            },

            removeItem: function () {
                var that = this;
                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!utils.csrfSafeMethod(settings.type) &&
                            utils.sameOrigin(settings.url)) {
                                
                            xhr.setRequestHeader("X-CSRFToken", 
                                utils.getCookie('csrftoken'));
                        }
                    }
                });
                $.ajax({
                    type: 'DELETE',
                    url: USER_GALLERY_URL,
                    data: {pk: that.model.get('id')},
                    success: function (resp) {
                        console.log(resp);
                        that.$el.fadeOut('slow');
                    },
                    error: function (err) {
                        console.log(err);
                    }
                });
            }
        }),

        MediaList = Backbone.Collection.extend({
            model: MediaItemModel,
            url: USER_GALLERY_URL
        }),

        Uploader = Backbone.View.extend({
            active: false,

            selected: null,

            el: '#media-upload-modal',

            initialize: function (options) {
                var that = this;
                this.options = options || {};
                that.$el.find('#tabs').tabs();
                that.$userGallery = that.$el.find('#tabs-2');
                that.$sBtn = that.$el.find('.submit-btn');
                that.dz = createDropzone();
                fetchGallery(function (items) {
                    that.collection = new MediaList(items);
                    that.render();
                    that.active = true;
                    that.listenTo(that.collection, 'reset', that.render);
                });
            },
            
            open: function () {
                this.$el.modal('show');
                this.collection.fetch();
            },

            refetch: function () {
                var that = this;
                that.$userGallery.empty();
                fetchGallery(function (items) {
                    that.collection.reset(items);
                    $('a[href="#tabs-2"]').trigger('click');
                });
            },

            render: function () {
                var that = this;
                this.collection.each(function (item) {
                    this.renderEntry(item);
                }, this);
                this.$el
                    .modal('show')
                    .data('mediaUploader', this)
                    .one('hidden.bs.modal', function () {
                        that.$userGallery.empty();
                    });
                this.$sBtn.one('click', function () {
                    if (typeof(that.options.callback) === 'function') {
                        that.options.callback(that.selected);
                    }
                    that.$el.modal('hide');
                });
            },

            renderEntry: function (item) {
                var that = this,
                    entry = new MediaItemView({
                        model: item
                    });
                $(entry.render().el)
                    .appendTo(this.$userGallery)
                    .bind('click', function () {
                        that.selected = entry.model.get('picture_url');
                        that.$el.find('.media-entry').removeClass('active');
                        entry.$el.addClass('active');
                    });
            }
        });
    
    return Uploader;
});