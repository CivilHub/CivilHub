//
// bookmarks.js
//
// Obsługa zakładek dla użytkownika

require(['jquery',
         'js/ui/ui'],

function ($, ui) {
    
    "use strict";
    
    $(document).delegate('.btn-add-bookmark, .btn-remove-bookmark', 'click',
    
        function (e) {
            e.preventDefault();
            
            var $button = $(e.currentTarget),
                text = '',
                msg = '',
                data = {
                    content_type: $button.attr('data-ct'),
                    object_id: $button.attr('data-id')
                };
                
            $.post('/api-userspace/bookmarks/', data, function (created) {
                text = (created) ? "Remove bookmark" : "Bookmark";
                msg = (created) ? "Bookmark added" : "Bookmark removed";
                $button
                    .toggleClass('btn-add-bookmark')
                    .toggleClass('btn-remove-bookmark')
                    .text(gettext(text));
                ui.message.success(msg);
            });
        }
    );
});