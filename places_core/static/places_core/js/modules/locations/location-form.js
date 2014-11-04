//
// location-form.js
// ================
//
// Skrypty obsługujące formularz dodawania nowej lokalizacji.

define(['jquery',
        'underscore',
        'backbone',
        'bootstrap-fileinput',
        'js/modules/ui/mapinput'],

function ($, _, Backbone) {
    
    "use strict";
    
    // Templatka dla dodawanych elementów formularza
    var inputTemplate = '<div class="fake-input"><select class="form-control">\
                         </select></div>';
    
    // Templatka dla pojedynczej opcji w elemencie 'select' (lokalizacja)
    var optionTemplate = '<option value="<%= id %>"><%= name %></option>';
    
    // Templatka dla 'sztucznego' elementu input zastępującego oryginalny select
    var textTemplate = '<input type="text" name="parent" id="id_parent" value=\
                        "<%= value %>" style="display:none;" />';
    
    // Element wyświetlający aktualnie wybrane miejsce
    var $indicator = $('<input type="text" />');
    $indicator.attr('readonly', 'readonly').addClass('form-control indicator');
    
    //
    // Location form
    // -------------
    
    var LocationForm = Backbone.View.extend({
        
        el:  "#new-location-form",
        
        initialize: function () {
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
            this.$fakeInput = $(_.template(inputTemplate, {}));
            // Przechowujemy wartość pola w formularzu do wysłania
            this.$realInput = $(_.template(textTemplate, {
                value: value
            }));
            
            // Wypełniamy pierwszy select WYŁĄCZNIE krajami
            _.each(window.COUNTRIES, function (country) {
                var $opt = $(_.template(optionTemplate, country));
                this.$fakeInput.find('select').append($opt);
            }, this);
            
            // Przygotowujemy DOM i przypinamy eventy
            $('#id_parent').replaceWith(this.$realInput);
            this.$indicator = $indicator;
            this.$fakeInput.insertAfter(this.$realInput);
            this.$indicator.insertAfter(this.$fakeInput);
            this.bindEvents(this.$fakeInput);
        },
        
        // Metoda tworząca kolejny 'sztuczny' input
        //
        // @param id { int } - pk localizacji, której "dzieci" chcemy pobrać
        
        expand: function (id) {
            
            var $fake = $(_.template(inputTemplate, {}));
            
            this.$realInput.val(id);

            $.get('/api-locations/sublocations/?pk='+id, function (response) {
                // Nie tworzymy nowego elementu, jeżeli lista jest już pusta
                if (response.length > 0) {
                    
                    $fake.insertBefore(this.$indicator);
                        
                    _.each(response, function (item) {
                        $fake.find('select')
                            .append(_.template(optionTemplate, item));
                    });
                    
                    this.bindEvents($fake);
                }
            }.bind(this));
        },
        
        // Metoda, która 'przypina' eventy do sztucznego elementu 'select'.
        //
        // @param $input { jQuery object } Element z 'inputTemplate'
        
        bindEvents: function ($input) {
            $input.find('select').on('click', function (e) {
                var $select = $input.find('select');
                
                var value = $select.find('option:selected').val();
                    
                $input.nextAll('.fake-input').empty().remove();
                
                this.expand(value);
                
                this.$indicator
                    .val($input.find('option:selected').text());
                    
            }.bind(this));
        }
    });
    
    return LocationForm;
});