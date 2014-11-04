//
// media-uploader.js
// =================
//
// Okno w modalu z obsługą galerii użytkownika. Umożliwia upload i usuwanie
// obrazów w galerii użytkownika, który ma aktywną sesję. Do działania potrzebuje
// templatki z pliku /templates/gallery/media-uploader.html.
// -----------------------------------------------------------------------------

define(['jquery',
        'underscore',
        'backbone',
        'dropzone'],

function ($, _, Backbone, Dropzone) {
    
    "use strict";
    
    // Pozwala uniknąć błędu 'dropzone already attached'
    Dropzone.autodiscover = false;
    
    //
    // MediaModel
    // ==========
    
    var MediaModel = Backbone.Model.extend({
        // Dodajemy slash na końcu adresu ze względu na zabezpieczenia Django
        url: function() {
            var original_url = Backbone.Model.prototype.url.call(this),
                parsed_url = original_url + (original_url.charAt(original_url.length - 1) == '/' ? '' : '/');

            return parsed_url;
        } 
    });
    
    //
    // MediaCollection
    // ===============
    
    var MediaCollection = Backbone.Collection.extend({
        
        model: MediaModel,
        
        url: '/api-gallery/usermedia/',
        
        initialize: function () {
            // Konieczne ze względu na Django csrf protection
            $.ajaxSetup({
                headers: {'X-CSRFToken': getCookie('csrftoken')}
            });
        }
    });
    
    //
    // MediaItem
    // =========
    // Widok dla pojedynczego elementu kolekcji (zdjęcia)
    
    var MediaItem = Backbone.View.extend({
        
        tagName: 'div',
        
        className: 'media-entry',

        template:  _.template($('#media-item-tpl').html()),

        events: {
            'click .delete-item-button': 'remove'
        },
        
        isActive: false, // Oznaczamy element jako aktywny/podświetlony

        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            // Podświetl element wybrany przez użytkownika
            this.$el.on('click', function (e) {
                e.preventDefault();
                // Odwołujemy się do widoku całego okna, zaznaczamy aktywny
                // element i odznaczamy wszystkie pozostałe.
                this.parentView.markSelected(this);
            }.bind(this));
            return this;
        },
        
        activate: function () {
            this.$el.addClass('active');
            this.isActive = true;
        },
        
        deactivate: function () {
            this.$el.removeClass('active');
            this.isActive = false;
        },
        
        remove: function () {
            // Usuwamy element. Sprawdzamy, czy jest aktualnie wybranym elemen-
            // tem i jeżeli tak, resetujemy aktywny element.
            if (this.parentView.selected === this) {
                this.parentView.selected = null;
            }
            this.model.destroy();
            this.$el.fadeOut('slow', function () {
                this.$el.empty().remove();
            }.bind(this));
        }
    });
    
    //
    // Uploader
    // ========
    // Główny widok aplikacji powązany z oknem modalu.
    
    var Uploader = Backbone.View.extend({
        
        el: '#media-upload-modal',
        
        selected: null,
        
        items: {}, // Przechowuje listę widoków powiązanych z modelami przez ID
        
        // Dodatkowe opcje dla uploadera. Tutaj możemy ustawić callback zewnętrz-
        // nej aplikacji, np. funkcję dodającą wybrany obrazek w edytorze. Do
        // funckcji zostanie przekazany aktualnie wybrany model.
        options: {
            onSubmit: function (item) {
                console.log(item);
            }
        },
        
        // Inicjalizacj aplikacji. Do metody można przekazać dodatkowe parametry
        // w postaci obiektu. Najczęściej wykorzystywaną będzie callback onSubmit.
        initialize: function (options) {
            
            var url = ''; // Url kolekcji do przekazania dla Dropzone.
            
            // Nadpisujemy domyślne opcje jeżeli użytkownik zdefiniował własne.
            _.extend(this.options, options);
            
            // Przygotowanie DOM
            this.$el.modal({show:false});
            this.$el.find('#tabs').tabs();
            this.collection = new MediaCollection();
            this.listenTo(this.collection, 'add', this.renderItem);
            this.$submit = this.$el.find('.submit-btn');
            this.collection.fetch();
            // Submitowanie formularza - wybieramy obrazek i przekazujemy go
            // do callbacku.
            this.$submit.on('click', function (e) {
                e.preventDefault();
                this.submit();
            }.bind(this));
            
            // Przygotowanie elementu Dropzone (uploadera)
            url = this.collection.url;
            this.dropzone = new Dropzone('#dropzone-input', {url: url});
            this.dropzone.on('complete', function () {
                // Dodaj zdjęcia uploadowane przez użytkownika, wyświetl je
                // w galerii i otwórz zakładkę ze zdjęciami.
                this.collection.fetch();
                this.$el.find('[href="#tabs-2"]').trigger('click');
            }.bind(this));
            // Hack w celu uniknięcia błędu 'dropzone already attached'
            $('#dropzone-input').addClass('dropzone');
        },
        
        renderItems: function (items) {
            items.each(function (item) {
                this.renderItem(item);
            }, this);
        },
        
        renderItem: function (item) {
            var picture = new MediaItem({
                model: item
            });
            picture.parentView = this;
            $(picture.render().el).appendTo(this.$el.find('#tabs-2'));
            // Tutaj łączymy widok z elementem kolekcji.
            this.items[item.get('id')] = picture;
        },
        
        markSelected: function (view) {
            // Metoda pozwalająca zaznaczyć (wybrać) obrazek z kolekcji. Jeżeli
            // nie przekażemy żadnego widoku (z listy this.items), wszystkie
            // aktywne elementy zostaną odznaczone.
            var view = view || false;
            
            this.seleted = null;
            
            // Odznaczamy nieaktywne elementy.
            _.each(this.items, function (item) {
                if (item.isActive) {
                    item.deactivate();
                }
            }, this);
            
            // Jeżeli użytkownik kliknął na obrazek w galerii, wybieramy go.
            if (view) {
                this.selected = view;
                view.activate();
            }
        },
        
        submit: function () {
            // Użytkownik wybrał obrazek i submitował formularz.
            if (typeof(this.options.onSubmit) === 'function') {
                var picture = {url: '', name: ''};
                if (!_.isNull(this.selected)) {
                    picture = this.selected.model.attributes;
                }
                this.options.onSubmit(picture);
            }
        },
        
        open: function () {
            // Pokazuje okno uploadera.
            this.$el.modal('show');
        },
        
        close: function () {
            // Zamykamy okno i resetujemy stan. Z niewiadomych powodów metoda
            // markSelected nie działa tutaj zgodnie z oczekiwaniami.
            this.$el.modal('hide');
            this.markSelected();
        }
    });
    
    return Uploader;
}); 