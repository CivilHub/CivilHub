//
// run-lightbox.js
// ===============

// Launches jsOnlyLightbox for chosen elements.

require(['jquery', 'lightbox'],

function ($, Lightbox) {

"use strict";

$(document).ready(function () {
  var lightbox = new Lightbox();
  lightbox.load();
});

});
