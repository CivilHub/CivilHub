//
// gallery.js
// ============

// Location gallery powred by masonry

require(['jquery',
	     'masonry'],

function ($, Masonry) {

"use strict";

$(document).ready(function () {
	$('.civgrid').show().prev('.m-gallery-loader').empty().remove();
	var msnry = new Masonry( '.civgrid', {
	});
});

});
