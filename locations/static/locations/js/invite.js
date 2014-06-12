(function ($) {
    
"use strict";
//
// Handle 'Invite User' system.
// -----------------------------------------------------------------------------
var $modal = $('#modal'),
    apiUrl = window.API_URL;

$modal.modal({show:false});

$.get(apiUrl, function (data) {
    // Load form into modal window.
    $modal.html(data)
        .find('.submit-btn')
        .bind('click', function (evt) {
            evt.preventDefault();
            sendAjaxRequest('POST', apiUrl, {
                data: {
                    'user': $('#id_user').val(),
                    'location': $('#id_location').val()
                },
                success: function (resp) {
                    display_alert(resp.message, resp.level);
                    $modal.modal('hide');
                },
                error: function (err) {
                    console.log(err);
                }
            });
        });
});

$('.invite-toggle')
    .tooltip()
    .bind('click',
        function (evt) {
            evt.preventDefault();
            $modal.modal('show');
        }
    );
    
})(jQuery);