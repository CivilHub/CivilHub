//
// ideas.js
// ========
// Run idea list.
require(['jquery',
         'js/modules/ideas/idea-list/ideaList'],

function ($, IdeaList) {
    
    "use strict";
    
    // Initialize list.
    // -------------------------------------------------------------------------
    var ideas = new IdeaList();
    
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

        ideas.filter();
    });
    //
    // Zapisanie formularza.
    // ---------------------
    // W taki sam sposób jak powyżej, łączymy submit formularza.
    //
    $('#haystack-form').bind('submit', function (e) {
        e.preventDefault();
        ideas.filter();
    });
});