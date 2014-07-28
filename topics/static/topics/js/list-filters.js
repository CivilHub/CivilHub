//
// Sortowanie listy dyskusji
// -----------------------------------------------------------------------------
//
(function ($) {
    "use strict";
    //
    // Funkcja pobierająca dodatkowe dane z formularza 'search'.
    // ---------------------------------------------------------
    function getSearchText() {
        var $field = $('#id_q'),
            txt = $field.val();
        
        if (_.isUndefined(txt) || txt.length <= 1) {
            return false;
        }
        
        return txt;
    }
    //
    // Wczytanie wybranych opcji.
    // ---------------------------
    // Sprawdzenie aktywnych elementów (klikniętych linków)
    // w celu "pozbierania" opcji wyszukiwarki.
    // 
    function getListOptions () {
        var $sel = $('.forum-list-control'),
            opts = {},
            optType = null,
            optValue = null;
        
        $sel.each(function () {
            var $this = $(this);
            
            if ($this.hasClass('active')) {
                optType = $this.attr('data-control');
                optValue = $this.attr('data-target');
                opts[optType] = optValue;
            }
        });
        
        opts['text'] = getSearchText();
        
        return opts;
    }
    //
    // Wczytanie opcji startowych.
    // ---------------------------
    // Parsowanie aktywnego url-a w celu ustawienia aktywnych
    // elementów w oparciu o wybrane opcje.
    //
    function loadListOptions() {
        var $sel = $('.forum-list-control'),
            data = urlToJSON(document.location.href);

        if (_.isEmpty(data)) {
            return true;
        }

        $sel.each(function () {
            var key = $(this).attr('data-control'),
                val = $(this).attr('data-target'),
                selected = data[key];
            
            if (val === selected) {
                $(this).addClass('active');
            } else {
                $(this).removeClass('active');
            }
        });
    }
    //
    // Obsługa kliknięć.
    // -----------------
    // Po kliknięciu na aktywny link w formularzu ta funkcja
    // zbiera wybrane opcje i tworzy URL do przekierowania.
    $('.forum-list-control').bind('click', function (evt) {
        var selectedItem = $(this).attr('data-control'),
            options = {},
            url     = '';
            
        evt.preventDefault();
        
        $('.active[data-control="' + selectedItem + '"]')
            .removeClass('active');
        $(this).addClass('active');
        
        options = getListOptions();
        url = $('#discussion-target-url').val() + JSONtoUrl(options);
        
        document.location.href = url;
    });
    $('#search-form').bind('submit', function (evt) {
        var options = getListOptions();
        evt.preventDefault();
        document.location.href =
            $('#discussion-target-url').val() + JSONtoUrl(getListOptions());
    });
    // Wczytanie początkowych ustawień.
    loadListOptions();
})(jQuery);