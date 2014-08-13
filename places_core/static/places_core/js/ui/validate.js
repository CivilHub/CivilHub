//
// validate.js
// ===========
// Simple validation for registration form.
//
require(['jquery', 'bootstrap'], function ($) {
    
    "use strict";
    
    var checkValidEmail = function (email, success, error) {
        $.ajax({
            type: 'GET',
            url: '/api-userspace/credentials/',
            data: {email: email},
            success: function (resp) {
                if (resp.valid && typeof(success) === 'function')
                    success(resp);
                else if (!resp.valid && typeof(error) === 'function')
                    error(resp);
            },
            error: function (err) {
                console.log(err);
            }
        });
    };
    
    var checkValidUsername = function (username, success, error) {
        $.ajax({
            type: 'GET',
            url: '/api-userspace/credentials/',
            data: {uname: username},
            success: function (resp) {
                if (resp.valid && typeof(success) === 'function')
                    success(resp);
                else if (!resp.valid && typeof(error) === 'function')
                    error(resp);
            },
            error: function (err) {
                console.log(err);
            }
        });
    };
    
    var displayErrors = function ($input, errorMsg) {
        if ($input.data('error')) {
            $input.popover('destroy');
        }
        $input.popover({content: errorMsg, trigger: 'manual'});
        $input.popover('show');
        $input.data('error', true);
    };
    
    $.fn.validateRegisterForm = function () {
        
        return $(this).each(function () {
            
            var $form = $(this),
                $uname = $(this).find('#username'),
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
                    displayErrors($input, gettext("This field cannot be empty!"))
                    errflag = true;
                    // Nie sprawdzamy już kolejnych pól
                    return false;
                }
            });
            
            // Sprawdzenie, czy adres email jest poprawnie sformatowany.
            if (!re.test($email.val())) {
                displayErrors($email, gettext("Must be valid email address"));
                errflag = true;
            }
            
            // Sprawdzenie, czy hasła zgadzają się ze sobą. Jeżeli nie, zostanie
            // wyświetlony komunikat, a same pola będą podświetlone.
            if ($pass1.val() != $pass2.val()) {
                displayErrors($pass2, gettext("Passwords don't match"));
                errflag = true;
            }
            
            if (!errflag) {
                checkValidUsername($uname.val(), null, function (err) {
                    displayErrors($uname, gettext("Username already taken"));
                });
            }
            
            if (!errflag) {
                checkValidEmail($email.val(), null, function (err) {
                    displayErrors($email, gettext("Email already taken"));
                });
            }
            
            // Jeżeli nie wyłapaliśmy żadnych błędów, wysyłamy formularz.
            if (!errflag) form.submit();
        });
    };
});