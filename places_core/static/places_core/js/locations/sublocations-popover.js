//
// sublocations-popover.js
// =======================
//
// Skrypty odpowiadające za wyświetlanie/filtrowanie menu sub-lokalizacji
// w pasku nawigacji w widoku lokalizacji.
//

require(['jquery'],

function ($) {
    
    "use strict";
    
    function filterList ($list, search) {
        var re = new RegExp(search, 'i');
        $list.find('.sublocation-list-entry').each(function () {
            if (re.test($(this).find('a:first').text())) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };
    
    $('.dropdown-title a').on('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).parent().find('.text-title').toggle();
        $(this).parent().find('.search-title').toggle();
    });
    
    $('.search-title input').on('click', function (e) {
        e.stopPropagation();
    });
    
    $('.search-title input').on('keyup', function (e) {
        filterList($(this).parents('.ancestors-menu:first'), $(this).val());
    });
    
    $('.search-title form').on('submit', function (e) {
        e.preventDefault();
    });
});