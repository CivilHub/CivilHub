//
// image-input.js
// ==============

// Plugin that enhance image file input and presents live preview
// of uploaded image. This is only module itself, it is wrapped in
// jQuery method in 'widgets' directory and applied on entire page.

define(['jquery',
        'underscore'],

function ($, _) {

"use strict";

// Wrapper that handles image selection.
//
// @param { DOM element } File input element
// @param { function }    Callback to trigger when image changes
// @param { object }      Context object to pass into callback

function getImageData (input, fn, ctx) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      if (_.isFunction(fn)) {
        fn.call(ctx, e.target.result);
      }
    };
    reader.readAsDataURL(input.files[0]);
  }
}

// Find for current image link if it's present
//
// We cannot rely on Django here, as ClearableFileInput doesn't provide
// any extra classes that could help us distinguish between regular image
// input and this enhanced version.
//
// @param { DOM Element }   File input element.
// @returns String | Boolean

function findCurrentImage (input) {
  var $links = $(input).siblings('a');
  var href = false;
  $links.each(function () {
    if (this.href.indexOf('.jpg') !== -1) {
      href = this.href;
    }
  });
  return href;
}

// Core program element - active input object itself.
//
// The only one mandatory option is 'el' and this should be DOM
// element for which this plugin instance should be initialized.
// The rest options passed will be ignored for now.

function ActiveInput (options) {
  this.$el = $(options.el);
  this.$preview = $('<div class="a-img-prev"></div>');
  this.$preview.insertAfter(this.$el);
  this.$el.on('change', this.selectImage.bind(this));
  this.fillImage();
}

// Check if initial image exists and display it if so.

ActiveInput.prototype.fillImage = function () {
  var link = findCurrentImage(this.$el[0]);
  if (link) {
    this.createPreview(link);
  }
};

// Show uploaded image when input value changes.

ActiveInput.prototype.selectImage = function (e) {
  getImageData(this.$el[0], function (data) {
    this.createPreview(data);
  }, this);
};

// Display image thumbnail in preview area.
//
// @param { base64 | string }  Base64 encoded image data or link to image file.

ActiveInput.prototype.createPreview = function (imgData) {
  var prev = new Image();
  prev.src = imgData;
  this.$preview.empty().append(prev);
};

return ActiveInput;

});
