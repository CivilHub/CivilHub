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
	$('.no-entries').removeClass('hide');
	var msnry = new Masonry( '.civgrid', {
	});
});

});
