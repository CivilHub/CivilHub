(function ($) {
    "use strict";
    //
    // Crete new category for forum topics
    // -----------------------------------
    //
    $('.btn-category-create').on('click', function (evt) {
        var form = _.template($('#category-form').html(), {}),
            $tpl = $(_.template($('#form-modal').html(), {
                title: "Add category",
                form: form
            })),
            $modal = $('#pl-modal'),
            formData = {};
            
        evt.preventDefault();
        
        $modal.html($tpl).modal('show');
        $modal.one('shown.bs.modal', function () {
            $modal.find('textarea').on('focus', function () {
                $(this).val('');
            });
            $modal.find('.btn-modal-submit').on('click', function () {
                $modal.find('form:first').submit();
            });
            $modal.find('form').on('submit', function (evt) {
                evt.preventDefault();
                formData = {
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                    name: $('#name').val(),
                    description: $('#description').val()
                }
                $.ajax({
                    type: 'POST',
                    url: '/rest/categories/',
                    data: formData,
                    success: function (data) {
                        display_alert(gettext('New category added'), 'success');
                        $modal.modal('hide');
                    },
                    error: function (err) {
                        alert('Test');
                        var $alert = $('<div class="alert alert-danger"></div>'),
                            desc = err.responseJSON.description;
                        $alert.appendTo($form.find('.form-group:first'))
                            .text(err.desc);
                    }
                });
            });
        });
        $modal.one('hidden.bs.modal', function () {
            $modal.empty();
        });
    });
})(jQuery);