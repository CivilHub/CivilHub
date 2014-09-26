//
//
//

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 300,
    
    paths: {
        async: 'includes/require/async',
        jquery: 'includes/jquery/jquery',
        jqueryui: 'includes/jquery-ui/jquery-ui',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        bootstrap: 'includes/bootstrap/bootstrap',
        bootbox: 'includes/bootstrap/bootbox'
    },
    
    shim: {
        underscore: {
            deps: ['jquery'],
            exports: '_'
        },
        
        backbone: {
            deps: ['underscore'],
            exports: 'Backbone'
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        jqueryui: {
            deps: ['jquery']
        }
    }
});

// Testujemy kontakty google+
function testGoogle () {
    var token = {
            access_token: window.GOOGLE_TOKEN,
            client_id: window.GOOGLE_KEY
        }

    $.ajax({
        url: 'https://www.google.com/m8/feeds/contacts/default/full',
        dataType: 'jsonp',
        data: token,
        success: function(data) { 
            console.log(data);
            alert("Contacts fetched!");
        }
    });
}

require(['jquery', 
         'jqueryui',
         'js/common',
         'async!https://apis.google.com/js/plusone.js',
         'async!https://plus.google.com/js/client:plusone.js?onload=testGoogle'],

function ($) {
    
    "use strict";
    
    $('#id_avatar').on('change', function (e) {
        $('#upload-avatar-form').submit();
    });
    
    $('#birth-date').datepicker({
        changeMonth: true,
        changeYear: true,
        minDate: new Date(1920, 1 - 1, 1),
        maxDate: 0,
        dateFormat: 'dd/mm/yy'
    });
    
    $('.simple-tabs-link').on('click', function (e) {
        e.preventDefault();
        var id = $(this).attr('data-target');
        if ($('#'+id).hasClass('active')) {
            return false;
        }
        $('.simple-tabs-tab').removeClass('active');
        $('#'+id).addClass('active');
    });
    
    $(document).trigger('load');
    
});
