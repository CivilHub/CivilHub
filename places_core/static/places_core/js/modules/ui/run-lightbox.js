//
// run-lightbox.js
// ===============

// Uruchamia jsOnlyLightbox dla wybranych elementów.

require(['jquery', 'lightbox'],

function ($, Lightbox) {
	"use strict";
	$(document).ready(function () {
		var lightbox = new Lightbox();
		lightbox.load();
	});
});
