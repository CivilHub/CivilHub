//
// location-form.js
// ================
//

require(['jquery',
        'underscore',
        'mapinput',
        'bootstrap-fileinput'],

function ($) {
    
    "use strict";
    
    var inputTemplate = '<label>&nbsp</label><select class="form-control \
                        fake-input"></select>';
    
    var optionTemplate = '<option value="<%= id %>"><%= name %></option>';
    
    var ActiveInput = function () {
        this.$el = $(_.template(inputTemplate, {}));
    };
    
    $(document).ready(function () {
        
        var $form = $('#new-location-form'),
            $real = $form.find('#id_parent'),
            $input = new ActiveInput();
        
        $form.find('[type="file"]').bootstrapFileInput();
        $form.find('#id_latitude').before('<div id="map"></div>');
        $form.find('#id_latitude, #id_longitude').css('display', 'none');
        $form.find('#map').mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 640,
                height: 480
            });
            
        $real.replaceWith('<input type="text" id="id_parent" style="display:none" />');
    });
    /*
    var LocationForm = Backbone.View.extend({
        
        el:  "#new-location-form",
        
        initialize: function () {
            this.$el.find('[type="file"]').bootstrapFileInput();
            this.$el.find('#id_latitude').before('<div id="map"></div>');
            this.$el.find('#id_latitude, #id_longitude').css('display', 'none');
            this.$el.find('#map').mapinput({
                latField: '#id_latitude',
                lngField: '#id_longitude',
                width: 640,
                height: 480
            });
            
            this.$realInput = this.$el.find('#id_parent');
            this.$indicator = $(document.createElement('p'));
            this.$fakeInput = $(document.createElement('select'));
            this.$realInput.css('display', 'none');
            this.$fakeInput
                .insertAfter(this.$realInput)
                .html(this.$realInput.html())
                .addClass('form-control fake-input');
            this.$indicator.insertBefore(this.$fakeInput);
            this.bindEvents(this.$fakeInput);
        },
        
        expand: function (id) {
            
            var $fake = $(document.createElement('select'));

            $.get('/api-locations/sublocations/?pk='+id, function (response) {
                if (response.length > 0) {
                    
                    $fake.insertAfter(this.$el.find('.fake-input:last'))
                        .addClass('form-control fake-input');
                        
                    _.each(response, function (item) {
                        $fake.append(_.template(optionTemplate, item));
                    });
                    
                    this.bindEvents($fake);
                }
            }.bind(this));
        },
        
        bindEvents: function ($input) {
            
            var self = this;
            
            $input.click(function() {
                if ($(this).data('clicks') == 1) {
                    $(this).nextAll('.fake-input').empty().remove();
                    self.expand($(this).val());
                    self.$realInput.val($(this).val());
                    self.$indicator.text($input.find('option:selected').text());
                    $(this).data('clicks', 0);
                } else {
                    $(this).data('clicks', 1);
                }
            });
            
            $input.focusout( function() {
                $(this).data('clicks', 0);
            });
        }
    });
    
    return LocationForm;*/
});