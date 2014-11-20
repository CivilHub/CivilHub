//
// discussions.js
// ==============
// Entry point for topics list application.
require(['js/modules/topics/discussion-list/discussionList'],

function (DiscussionList) {
    
    "use strict";
    
    function getCategoryId () {
        var re = /#[0-9]+/,
            res = re.exec(document.location.href);
        if (res !== null) {
            return res[0].replace('#', '');
        }
        return null;
    }
    
    var discussions = new DiscussionList({'cat': getCategoryId()});
    
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