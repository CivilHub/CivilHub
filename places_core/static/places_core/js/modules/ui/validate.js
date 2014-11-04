//
// validate.js
// ===========
//
// Prosta walidacja dla formularza rejestracji. Skrypt sprawdza, czy wszystkie
// pola są wypełnione (zakładamy, że wszystkie są wymagane), po czym wywołuje
// po kolei walidację wszystkich pól, sprawdzając przy okazji dostępność adresu
// email i nazwy użytkownika. 
// 
// TODO: Na chwilę obecną jedyny błąd, jaki nie zostanie
// przechwycony w przeglądarce, to nieprawidłowa nazwa użytkownika. Wówczas 
// strona zostanie przeładowana i dopiero pojawi się informacja o błędzie.
//
require(['jquery'], function ($) {
    
    "use strict";
    
    // Regex sprawdzający poprawność adresów email
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    
    // checkCredentials
    // ----------------
    // Funkcja sprawdzająca dostępność adresu email lub nazwy użytkownika.
    //
    // @param data    { object }   Dane do zapytania (email lub username),
    //                              np: ```{'email':'tester@test.com'}```
    // @param valid   { function } Callback w przypadku dostępności elementu
    // @param invalid { function } Callback do wywołania, kiedy element nie jest
    //                              dostępny.
    var checkCredentials = function (data, valid, invalid) {
        $.get('/api-userspace/credentials/', data, function (resp) {
            if (resp.valid === true && typeof(valid) === 'function') {
                valid(resp);
            } else if (resp.valid === false && typeof(invalid) === 'function') {
                invalid(resp);
            }
        });
    };
    
    // Validator
    // ---------
    // Klasa ułatwiająca walidację. Inicjalizując walidator przekazujemy for-
    // mularz w formie obiektu jQuery. Udostępnia metodę `validate`, którą 
    // należy zastosować przed submitowaniem formy.
    //
    function Validator ($form) {
        this.$el     = $form;
        this.fields  = $form.find('input');
        this.$submit = $form.find('[type="submit"]');
        this.errors  = [];
    };
    
    Validator.prototype.displayErrors = function () {
        var errors = this.errors,
            $form  = this.$el,
            $input = null;

        for (var i = 0; i < errors.length; i++) {
            $input = $form.find('#' + errors[i].label);
            $form.find('#' + errors[i].label).popover({
                content: errors[i].message,
                placement: 'left'
            });
            $input.popover('show');
        }
    };
    
    Validator.prototype.clearErrors = function () {
        this.errors = [];
        this.fields.each(function () {
            $(this).popover('destroy');
        });
    };
    
    Validator.prototype.validateField = function ($field) {
        var label = $field.attr('id'),
            value = $field.val(),
            errors = this.errors;

        if (!value) {
            
            errors.push({label: label, message: gettext("This field is required")});
            
        } else {
            
            if (label == 'username') {
                checkCredentials({uname:value}, null, function () {
                    errors.push({label: label, message: gettext("Username already exists")});
                });
            }
            
            if (label == 'email') {
                if (!re.test(value)) {
                    errors.push({label: label, message: gettext("Invalid email address")});
                } else {
                    checkCredentials({email:value}, null, function () {
                        errors.push({label: label, message: gettext("Email already taken")});
                    });
                }
            }
            
            if (label == 'pass2' && $('#pass1').val() != $('#pass2').val()) {
                errors.push({label: label, message: gettext("Passwords don't match")});
            }
        }
    };
    
    Validator.prototype.performValidation = function () {
        var self = this;
        this.clearErrors();
        this.fields.each(function () {
            self.validateField($(this));
        });
    };
    
    Validator.prototype.validate = function () {
        var self = this;
        this.performValidation();
        setTimeout(function () {
            if (self.errors.length > 0) {
                self.displayErrors();
            } else {
                self.$el.submit();
            };
        }, 1000);
    };
    
    //
    // registerFormValidator
    // ---------------------
    // Plugin jQuery, który tworzy walidator dla formularza rejestracji.
    $.fn.registerFormValidator = function () {
        
        return $(this).each(function () {
            
            var $form = $(this),
                v = new Validator($form);

            $('#signup_button').on('click', function (e) {
                e.preventDefault();
                v.validate();
            });
            
            $form.data('validator', v);
        });
    };
});