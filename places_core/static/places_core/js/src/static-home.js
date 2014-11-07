/*
 * static-home.js
 * ==============
 * 
 * Strona domowa i formularz rejestracji.
 * 
 * TODO: formularz rejestracji waliduje się przez JS tylko po kliknięciu
 * przycisku do submitowania. Po naciśnięciu 'ENTER' strona się przeładowuje
 * bez względu na aktualną zawartość formularza.
 */

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery     : "includes/jquery/jquery",
        jpaginate  : "includes/jquery/jquery.paginate",
        bootstrap  : "includes/bootstrap/bootstrap",
        bootbox    : "includes/bootstrap/bootbox",
        underscore : "includes/underscore/underscore",
        backbone   : "includes/backbone/backbone"
    },
    
    shim: {
        
        jpaginate: {
            deps: ["jquery"]
        },
        
        bootstrap: {
            deps: ["jquery"]
        },
        
        underscore: {
            deps: ["jquery"],
            exports: "_"
        },
        
        backbone: {
            deps: ["underscore"],
            exports: "Backbone"
        },
        
        bootbox: {
            deps: ["bootstrap"],
            exports: "bootbox"
        }
    }
});

require(['jquery',
         'bootstrap',
         'js/modules/common',
         'js/modules/ui/validate'],

function ($) {
    
    "use strict";
    
    $('#pl-register-form').registerFormValidator();
    
    $(document).trigger('load');
    
});