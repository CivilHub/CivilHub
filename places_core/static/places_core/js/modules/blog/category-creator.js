//
// category-creator.js
// ===================
// Create new blog category.

require(['jquery',
         'js/modules/ui/categoryForm'],

function ($, CategoryForm) {
    
    "use strict";
    
    var BlogCategoryForm = CategoryForm.extend({
        baseurl: '/rest/categories/'
    });
    
    var form = new BlogCategoryForm();
    
    $('.btn-category-create').on('click', function (e) {
        e.preventDefault();
        form.open();
    });
});