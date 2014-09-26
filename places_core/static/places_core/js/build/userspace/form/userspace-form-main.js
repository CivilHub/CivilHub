//
//
//

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 300,
    
    paths: {
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

require(['jquery',
         'jqueryui',
         'js/common'],

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
