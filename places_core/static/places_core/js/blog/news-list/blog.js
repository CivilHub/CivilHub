//
// blog.js
// =======
//
// Run scripts for location's blog.
//
require(['js/blog/news-list/news-list'], function (NewsList) {
    
    // Initialize list.
    // -------------------------------------------------------------------------
    var blog = new NewsList();

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

        blog.filter();
    });
    //
    // Zapisanie formularza.
    // ---------------------
    // W taki sam sposób jak powyżej, łączymy submit formularza.
    //
    $('#haystack-form').bind('submit', function (e) {
        e.preventDefault();
        blog.filter();
    });
});