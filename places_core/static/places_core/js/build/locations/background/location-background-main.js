//
// Formularz zmiany obrazu tła dla użytkownika.
//
//  => /templates/userspace/background-form.html
//

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox',
        color: 'includes/jquery/jquery.color',
        Jcrop: 'includes/jquery/jquery.Jcrop',
        'file-input': 'includes/bootstrap/bootstrap.file-input'
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
        
        tagsinput: {
            deps: ['jquery']
        },
        
        color: {
            deps: ['jquery']
        },
        
        Jcrop: {
            deps: ['color']
        },
        
        'file-input': {
            deps: ['bootstrap']
        }
    }
});

require(['jquery',
         'js/ui/image-form',
         'js/common'],

function($, ImageForm) {
    
    "use strict";
    
    $(document).ready(function () {
        var form = new ImageForm({
            $el: $('#user-background-form'),
            orientation: 'landscape'
        });
        window.test = form;
    });
    
    $(document).trigger('load');
    
});