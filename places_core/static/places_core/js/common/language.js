//
// language.js
// ===========
//
// Popover pozwalający użytkownikowi wybrać język witryny
//
// ------------------------------------------------------

require(['jquery',
         'bootstrap'],

function ($) {
    
    "use strict";
    
    $(document).ready(function () {
        
        $("#lang-selector").popover({
            html : true, 
            content: function() {
                $('#lang-list > li').each(function() {
                    var currentLang = $('#lang-list').attr('data-current-lang');
                    if( $(this).attr('data-code') === currentLang ) {
                        $(this).addClass('selected');
                    }
                });
                return $('#popover-lang-list').html();
                    },
            placement: "top"
        });

        $(document).delegate('#lang-list > li', 'click', function (e) {
            e.stopPropagation();
            e.preventDefault();
            var langCode = $(this).attr('data-code');
            if(langCode != undefined) {
                $('input[name="language"]').val(langCode);
                $('#lang-form').submit();
            }
            return false;
        });

        $('body').on('mouseup', function(e) {
            if(!$(e.target).closest('.popover').length) {
                $('.popover').each(function(){
                    $(this.previousSibling).popover('hide');
                });
            }
        });
    });
});