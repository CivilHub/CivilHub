//
// image-form.js
// =============
//
// Skrypty obsługujące formularz dodawania obrazów tła oraz avatara użytkownika.
//
// Do działania skryptu potrzebujemy gotowego formularza, który przekazujemy pod-
// czas inicjalizacji jako parametr `$el` - jQuery selector. Formularz musi
// mieć pole typu `file` z unikalnym parametrem `id` (obojętnie, jakim).
//
// Przykład zastosowania: var form = new ImageForm({$el: $('#myform')});


define(['jquery',
        'underscore',
        'Jcrop',
        'file-input'],

function ($, _) {
    
    "use strict";
    
    // Opcje domyślne (będzie tego więcej)
    // -----------------------------------
    
    var defaults = {
        orientation: 'landscape',
        maxWidth: 1024
    };
    
    // Oblicz rozmiar początkowej selekcji.
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
    // Główny obiekt formularza - inicjalizacja
    
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
    // Pobiera informacje o wybranym obrazie i wywołuje callback - zaznacza
    // przesłany obraz jako wybrany.
    
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
    // Wybór nowego obrazu. Funkcja updatuje podgląd i tworzy nowy obiekt Jcrop.
    //
    // @param imageData { string } - odkodowane informacje o obrazie.
    
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
    // "Czyścimy" DOM oraz eventy, w szczególności pozbywamy się istniejącej
    // instancji Jcrop.
    
    ImageForm.prototype.cleanup = function () {
        if (!_.isNull(this.jcrop)) {
            this.jcrop.destroy();
        }
        this.$preview.find('img').empty().remove();
    };
    
    // submit
    // ------
    // Wysłanie formularza na serwer.
    
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