//
// uploader.js
// ===========
//
// A Plugin for the editor Redaktor that allows for managing images in the gallery
// of the user through an external window modal. To launch the plugin we must
// "launch" the editor with certain options. It is worth mentioning that this
// file must be loaded BEFORE the editor itself will be loaded (redactor.js file)
// Else we will get an error "RedactorPlugins is undefined".


define(['js/modules/ui/media-uploader'],

function (Uploader) {

  "use strict";

  if (typeof(window.RedactorPlugins) === 'undefined')
      window.RedactorPlugins = {};

  var imgTemplate = '<img src="<%= picture_url %>" alt="<%= picture_name %>" />';

  var uploader = {

    init: function () {
      this.buttonAdd('uploader', 'Upload Media', this.openUploader);
      this.buttonAwesome('uploader', 'fa-file-image-o');
    },

    openUploader: function () {
      var self = this;
      if (typeof(this.uploader) === 'undefined') {
        this.uploader = new Uploader({
          onSubmit: function (picture) {
            self.insertImage(picture);
          }
        });
      }
      this.uploader.open();
    },

    insertImage: function (picture) {
      var html = imgTemplate
          .replace(/<%= picture_url %>/g, picture.picture_url)
          .replace(/<%= picture_name %>/g, picture.picture_name);

      this.insertHtml(html);
    }
  };

  window.RedactorPlugins.uploader = uploader;

  return uploader;
});
