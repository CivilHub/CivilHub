//
// discussionForm.js
// =================
//

(function ($) {
    
    "use strict";
    
    $(document).ready(function () {
        
        $('#id_description').redactor({
            //plugins: ['advanced']
        });
        
        $('#id_tags').tagsInput({
            autocompleteUrl: '/rest/tags/'
        });
    });
    
})(jQuery);