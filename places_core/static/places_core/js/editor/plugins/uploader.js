//
// uploader.js
// ===========
//
// Plugin dla edytora Redaktor umożliwiający zarządzanie zdjęciami w galerii
// użytkownika przez zewnętrzne okno modala. Abu uruchomić plugin, musimy
// "odpalić" edytor z odpowiednimi opcjami. Należy pamiętać o tym, że ten plik
// musi zostać wczytany ZANIM wczytany zostanie sam edytor (plik redactor.js).
// Inaczej wywali nam błąd 'RedactorPlugins is undefined'.

define(['js/ui/media-uploader'],

function (Uploader) {
    
    "use strict";
    
    if (typeof(window.RedactorPlugins) === 'undefined')
        window.RedactorPlugins = {};
        
    var imgTemplate = '<img src="<%= picture_url %>" alt="<%= picture_name %>" />';
    
    var uploader = {
        
        init: function() {
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