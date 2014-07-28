//
// Add ideas category.
// ===================
//
(function ($) {
"use strict";
$(document).ready(function () {
    var $modal = $('#new-category-form'),
        $form = $modal.find('form:first'),
        $sBtn = $modal.find('.submit-btn:first');

    $form.bind('submit', function (evt) {
        var data = {
                name: $('#category-name').val(),
                description: $('#category-description').val()
            };
        evt.preventDefault();
        sendAjaxRequest('POST', '/rest/ideas/', {
            data: data,
            success: function (resp) {
                display_alert(gettext("Category added"), 'success');
                $modal.modal('hide');
            },
            error: function (err) {
                var $alert = {},
                    errors = {},
                    error = null;
                try {
                    errors = err.responseJSON;
                    for (error in errors) {
                        if (errors.hasOwnProperty(error)) {
                            $alert = $('<div></div>');
                            $alert.prependTo($modal.find('.form-group:first'))
                                .text(error + ": " + errors[error])
                                .addClass('alert alert-danger');
                            console.log(error + ": " + errors[error]);
                        }
                    }
                } catch (err) {
                    console.log(err);
                }
            }
        });
    });

    $sBtn.bind('click', function (evt) {
        $form.submit();
    });

    $('.new-category-btn').bind('click', function (evt) {
        evt.preventDefault();
        $modal.modal('show');
    });
});
})(jQuery);