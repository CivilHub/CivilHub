//
// pollList.js
// ===========
// Application hook for poll list.
require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'js/modules/polls/poll-list/pollListView'],

function ($, _, utils, PollListView) {
    
    "use strict";
    
    var polls = new PollListView();
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

        polls.filter();
    });
    
    //
    // Zapisanie formularza.
    // ---------------------
    // W taki sam sposób jak powyżej, łączymy submit formularza.
    //
    $('#haystack-form').bind('submit', function (e) {
        e.preventDefault();
        polls.filter();
    });
});