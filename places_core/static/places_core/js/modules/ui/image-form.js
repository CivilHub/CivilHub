//
// image-form.js
// =============
//
// A script that takes care of adding additional background images and user avatars.
//
// In order for the script to work, we need a ready form that we send during
// initalization process as a parameter '$el' - jQuery selector. The form
// must have the field 'file' with a unique 'id' parameter (doesn't matter which
// exactly )
//
// Sample use: var form = new ImageForm({$el: $('#myform')});

define(['jquery',
        'underscore',
        'Jcrop',
        'file-input'],

function ($, _) {
    
    "use strict";
    
    // Default option (there is more to come)
    // -----------------------------------
    
    var defaults = {
        orientation: 'landscape',
        maxWidth: 1024
    };
    
    // calculate the base size of selection
    // ------------------------------------
    
    function calculateSelection (size, ratio) {
        
        var x, y, x2, y2;
        
        x = 0;
        x2 = size.width;
        var maxHeight = size.height / ratio;
        y = (size.height - maxHeight) / 2;
        y2 = y + maxHeight;
        
        return [x, y, x2, y2];
    }
    
    // ImageForm
    // =========
    // Main object form - initialization
    
    var ImageForm = function (options) {
        
        this.opts = _.extend(defaults, options);
        
        switch (this.opts.orientation) {
            case 'landscape':
                this.opts.aspectRatio = 19/3;
                break;
            default: this.opts.aspectRatio = 1/1;
        }
        
        this.$el = this.opts.$el;
        
        this.$preview = $('<div id="img-preview"></div>');
        
        this.$input = this.$el.find('[type=file]:first');
        
        this.$input.bootstrapFileInput();
        
        this.jcrop = null;
        
        this.$preview.insertBefore(this.$el);
        
        this.$el.find('[type=submit]').on('click', function (e) {
            e.preventDefault();
            this.submit();
        }.bind(this));
        
        this.$input.on('change', function (e) {
            e.preventDefault();
            this.getImageData();
            return false;
        }.bind(this));
    };
    
    // getImageData
    // ------------
    // Downloads information about a certain image and calls a callback -
    // marks the send image as selected.
    
    ImageForm.prototype.getImageData = function () {
        
        var input = document.getElementById(this.$input.attr('id'));
        var self = this;
        
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                self.selectImage(e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    };
    
    // selectImage
    // -----------
    // New image selection. This function updates the preview and creates a new
    // Jcrop object. 
    //
    // @param imageData { string } - decodes information about the image.
    
    ImageForm.prototype.selectImage = function (imageData) {
        var $img = $(document.createElement('img'));
        var self = this;
        this.cleanup();
        this.$preview.append($img);
        $img.attr('src', imageData);
        $img.Jcrop({
            aspectRatio: self.opts.aspectRatio,
            boxWidth: self.opts.maxWidth,
            setSelect: calculateSelection({
                    width: $img.width(),
                    height: $img.height(),
                }, self.opts.aspectRatio)
        }, function () {
            self.jcrop = this;
        });
    };
    
    // cleanup
    // -------
    // We "clean" the DOM and the events, in particular, we get rid of
    // existing jCrop instances
    
    ImageForm.prototype.cleanup = function () {
        if (!_.isNull(this.jcrop)) {
            this.jcrop.destroy();
        }
        this.$preview.find('img').empty().remove();
    };
    
    // submit
    // ------
    // Sends the from to the server.
    
    ImageForm.prototype.submit = function () {
        var formData = this.jcrop.tellSelect();
        this.$el.find('[name=x]').val(parseInt(formData.x, 10));
        this.$el.find('[name=y]').val(parseInt(formData.y, 10));
        this.$el.find('[name=x2]').val(parseInt(formData.x2, 10));
        this.$el.find('[name=y2]').val(parseInt(formData.y2, 10));
        this.$el.submit();
    };
    
    return ImageForm;
});