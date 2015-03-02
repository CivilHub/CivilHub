//
// category-creator.js
// ===================
// Create new forum category.

require(['jquery',
         'js/modules/ui/categoryForm'],

function ($, CategoryForm) {
    
    "use strict";
    
    var ForumCategoryForm = CategoryForm.extend({
        baseurl: '/rest/discussion/'
    });
    
    var form = new ForumCategoryForm();
    
    $('.new-category-btn').on('click', function (e) {
        e.preventDefault();
        form.open();
    });
});