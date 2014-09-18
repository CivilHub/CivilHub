//
// user-gallery-main.js
// ====================
//
// Skrypty dla głównego widoku galerii użytkownika.
//  => /templates/gallery/user-gallery.html

require.config({
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
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
        }
    }
});

require(['jquery',
         'js/ui/ui',
         'js/common'],

function ($, ui) {
    
    "use strict";
    
    function deletePicture (id) {
        $.ajaxSetup({
            headers: {'X-CSRFToken': getCookie('csrftoken')}
        });
        $.ajax({
            type: 'DELETE',
            url: '/api-gallery/usermedia/'+id+'/',
            success: function () {
                document.location.href = document.location.href;
            }
        });
    };
    
    $('.control-delete').on('click', function (e) {
        e.preventDefault();
        var id = $(this).attr('data-target');
        ui.confirmWindow(deletePicture, null, [id]);
    });
    
    $(document).trigger('load');
});