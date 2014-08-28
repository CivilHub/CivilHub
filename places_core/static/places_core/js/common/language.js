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
              return $('#popover-lang-list').html();
            },
            
            placement: "top"
        });
    });
});