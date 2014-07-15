//
// discussions.js
// ==============
// Entry point for topics list application.
require(['js/topics/discussion-list/discussionList',
         'js/ui/categoryForm'],

function (DiscussionList, CategoryForm) {
    "use strict";
    
    var Form = CategoryForm.extend({
        baseurl: '/rest/discussion/'
    });
    
    var categoryForm = new Form();
    
    var discussions = new DiscussionList();
    
    $('.new-category-btn').on('click', function (e) {
        categoryForm.open();
    });
    
    //
    // Obsługa kliknięć.
    // -----------------
    // Po kliknięciu na aktywny link w formularzu ta funkcja
    // zbiera wybrane opcje i tworzy URL do przekierowania.
    //
    $('.list-controller').bind('click', function (e) {
        var selectedItem = $(this).attr('data-control');

        e.preventDefault();

        $('.active[data-control="' + selectedItem + '"]')
            .removeClass('active');
        $(this).addClass('active');

        discussions.filter();
    });
    
    //
    // Zapisanie formularza.
    // ---------------------
    // W taki sam sposób jak powyżej, łączymy submit formularza.
    //
    $('#haystack-form').bind('submit', function (e) {
        e.preventDefault();
        discussions.filter();
    });
});