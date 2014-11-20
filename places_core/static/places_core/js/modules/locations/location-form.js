/**
 * location-form.js
 * ================
 *
 * Skrypty obsługujące formularz tworzenia lokalizacji.
 *
 * TODO: uzupełnianie początkowej wartości w formularzu.
 */

define(['jquery',
        'underscore',
        'backbone',
        'bootstrap-fileinput',
        'js/modules/ui/mapinput'],

function ($, _, Backbone) {
    
    "use strict";
    
    // Base sublocations API url
    
    var baseUrl = '/api-locations/sublocations/';
    
    // Domyślny tekst na przycisku aktywującym listę
    
    var defaultOpt = gettext("Click to select from list");
    
    // Szablon dla całej grupy "sztucznego" elementu
    // (załączony w locations/templates/locations/location_form.html)
    
    var inputTemplate = $('#input-tpl').html();
    
    // Templatka dla pojedynczej opcji w elemencie 'select' (lokalizacja)
    
    var optionTemplate = '<li class="name-entry" data-value="<%= id %>"><%= name %></li>';
    
    // Templatka dla 'sztucznego' elementu input zastępującego oryginalny select
    
    var textTemplate = '<input type="text" name="parent" id="id_parent" value=\
                        "<%= value %>" style="display:none;" />';

    // Element wyświetlający aktualnie wybrane miejsce
    
    var $indicator = $('<input type="text" />');
    $indicator.attr('readonly', 'readonly')
        .addClass('form-control indicator');
    
    // Single "fake" input element
    // ---------------------------
    
    var InputElement = Backbone.View.extend({
        
        className: 'fake-input',
        
        template: _.template(inputTemplate),
        
        events: {
            'click .name-entry': 'expand',
            'click .input-indicator': 'toggleList',
            'keyup .search-filter': 'filter'
        },
        
        initialize: function (data) {
            
            // parent odnosi się do nadrzędnego View (location-form). W ten
            // sposób zachowujemy wzajemną relację
            
            this.parent = data.parent || undefined;
            
            // parentId odnosi się do ID lokalizacji, której "dzieci" pobieramy
            
            this.parentId = data.parentId || null;
            
            // Lista sub-lokalizacji pobranych z serwera
            
            this.options = data.options || [];
        },
        
        renderOption: function (option) {
            var tpl = _.template(optionTemplate);
            this.$el.find('ul').append($(tpl(option)));
        },
        
        render: function () {
            if (this.options.length <= 0) {
                return false;
            }
            this.$el.html(this.template, null);
            _.each(this.options, function (option) {
                this.renderOption(option);
            }, this);
            this.select(defaultOpt);
            return this;
        },
        
        // Metoda przekazuje przechwycone kliknięcie do nadrzędnego widoku
        // i uaktualnia pola formularza oraz tworzy nowy sztuczny element.
        // FIXME: być może lepsze tu będzie propagowanie zdarzeń Backbone.
        
        expand: function (e) {
            var id = $(e.currentTarget).attr('data-value'),
                name = $(e.currentTarget).text();
            
            if (this.parent !== undefined) {
                this.$el.nextAll('.fake-input')
                    .empty().remove();
                this.parent.expand(id);
                $indicator.val(name);
                this.$el.find('.selected').removeClass('selected');
                $(e.currentTarget).addClass('selected');
                this.select(name);
                this.toggleList();
            }
        },
        
        // Metoda pokazuje/ukrywa listę sublokalizacji
        
        toggleList: function () {
            var $ul = this.$el.find('ul');
            $('ul.expanded').not($ul)
                .hide()
                .removeClass('expanded');
            this.$el.find('ul').toggle()
                .toggleClass('expanded');
        },
        
        /** 
         * Metoda uzupełnie aktualnie wybraną
         * lokalizację do wyświetlenia na przycisku
         *
         * @param name { string } Nazwa lokalizacji
         */
        
        select: function (name) {
            var $i = this.$el.find('.input-indicator');
            $i.text(name);
            if (name !== defaultOpt) {
                $i.removeClass('btn-success')
                    .addClass('btn-primary');
            }
        },
        
        // Metoda filtruje listę i ukrywa wyniki, które nie pasują
        
        filter: function () {
            var name = this.$el.find('.search-filter').val(),
                re = new RegExp(name, 'i');
            this.$el.find('.name-entry').each(function (item) {
                if (re.test($(this).text())) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        }
    });
    
    // Location form
    // -------------
    
    var LocationForm = Backbone.View.extend({
        
        el:  "#new-location-form",
        
        initialize: function () {
            
            var parent = this;
            
            this.$el.find('[type="file"]')
                .bootstrapFileInput();                  // Wybór zdjęcia
            this.$el.find('#id_latitude')
                .before('<div id="map"></div>');        // Minimapa
            this.$el.find('#id_latitude, #id_longitude')
                .css('display', 'none');
            this.$el.find('#map').mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 640,
                height: 480
            });
            
            var value = $('#id_parent').val();          // Startowa wartość
            
            // Pierwszy 'sztuczny' select
            
            this.$fakeInput = new InputElement({
                parent: parent,
                options: COUNTRIES
            });
            
            // Przechowujemy wartość pola w formularzu do wysłania
            
            this.$realInput = $(_.template(textTemplate, {
                value: value
            }));
            
            // Przygotowujemy DOM i przypinamy eventy
            
            $('#id_parent').replaceWith(this.$realInput);
            this.$indicator = $indicator;
            this.$indicator.insertAfter(this.$realInput);
            $(this.$fakeInput.render().el)
                .insertAfter(this.$realInput);
        },
        
        // Metoda tworząca kolejny 'sztuczny' input
        //
        // @param id { int } - pk localizacji, której "dzieci" chcemy pobrać
        
        expand: function (id) {
            
            var url = ([baseUrl, '?pk=', id]).join(''),
                fake = null,
                parent = this;
            
            $.get(url, function (response) {
                if (response.length <= 0) {
                    return false;
                }
                fake = new InputElement({
                    parent: parent,
                    parentId: id,
                    options: response
                });
                $(fake.render().el)
                    .insertAfter(this.$el.find('.fake-input').last());
            }.bind(this));
            
            this.$realInput.val(id);
            alert(this.$realInput.val());
        }
    });
    
    return LocationForm;
});