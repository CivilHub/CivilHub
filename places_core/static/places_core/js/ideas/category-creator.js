//
// category-creator.js
// ===================
// Create new ideas category.

require(['jquery',
         'js/ui/categoryForm'],

function ($, CategoryForm) {
    
    "use strict";
    
    var IdeaCategoryForm = CategoryForm.extend({
        baseurl: '/rest/idea_categories/'
    });
    
    var form = new IdeaCategoryForm();
    
    $('.new-category-btn').on('click', function (e) {
        e.preventDefault();
        form.open();
    });
});