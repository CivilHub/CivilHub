//
// validate.js
// ===========
// Simple validation for registration form.
//
require(['jquery', 'bootstrap'], function ($) {
    
    "use strict";
    
    var checkValidEmail = function (email) {
        
    };
    
    var checkValidUsername = function (username) {
        
    };
    
    $.fn.validateRegisterForm = function () {
        
        return $(this).each(function () {
            
            var $form = $(this),
                $email = $(this).find('#email'),
                $pass1 = $(this).find('#pass1'),
                $pass2 = $(this).find('#pass2'),
                errflag = false,
                re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

            // Sprawdzenie, czy wszystkie pola mają jakąś wartość. Ponieważ
            // wszystkie są wymagane, zatrzymujemy się na pierwszym pustym i wyś-
            // wietlamy komunikat
            $form.find('input').each(function () {
                var $input = $(this);
                if (!$input.val()) {
                    $input.popover({
                        content: gettext("This field cannot be empty!")
                    });
                    $input.popover('show');
                    errflag = true;
                    // Nie sprawdzamy już kolejnych pól
                    return false;
                }
            });
            
            // Sprawdzenie, czy adres email jest poprawnie sformatowany.
            if (!re.test($email.val())) {
                $email.popover({
                    content: gettext("Must be valid email address")
                });
                $email.popover('show');
                errflag = true;
            }
            
            // Sprawdzenie, czy hasła zgadzają się ze sobą. Jeżeli nie, zostanie
            // wyświetlony komunikat, a same pola będą podświetlone.
            if ($pass1.val() != $pass2.val()) {
                $pass2.popover({
                    content: gettext("Passwords don't match")
                });
                $pass2.popover('show');
                $pass1.addClass('has-error').removeClass('has-success');
                $pass2.addClass('has-error').removeClass('has-success');
                errflag = true;
            }
            
            // Sprawdzenie poprawności haseł w trakcie wpisywania. Jeżeli użyt-
            // kownik poprawnie powtórzy hasło, zostanie o tym poinformowany.
            $pass1.add($pass2).on('keyup', function (e) {
                if ($pass1.val() == $pass2.val()) {
                    $pass1.addClass('has-success').removeClass('has-error');
                    $pass2.addClass('has-success').removeClass('has-error');
                    $pass2.popover('destroy');
                }
            });
            
            // Sprawdzenie, czy adres email nie został już wykorzystany przez
            // kogoś innego.
            $email.on('focusout', function () {
                checkValidEmail(function () {
                        
                    }, function () {
                        
                    }
                });
            });
            
            // Sprawdzenie, czy nazwa użytkownika nie została już wykorzystana.
            $form.find('#username').on('focusout', function () {
                checkValidUsername(function () {
                        
                    }, function () {
                        
                    }
                });
            });
            
            // Jeżeli nie wyłapaliśmy żadnych błędów, wysyłamy formularz.
            if (!errflag) form.submit();
        });
    };
});