(function ($) {
    "use strict";
    //
    // Crete new category for newses
    // -----------------------------
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
                        display_alert('New category added', 'success');
                        $modal.modal('hide');
                    }
                });
            });
        });
        $modal.one('hidden.bs.modal', function () {
            $modal.empty();
        });
    });
})(jQuery);