//
// pointer.js
// ==========
// Script to load when you want to use map pointer form.
require(['maps/pointerModal'],

function (PointerModal) {
    "use strict";
    
    var pointer = new PointerModal();
    pointer.open();
});