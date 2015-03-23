//
// sublocations.js
// ===============

// Uruchamia popover z sublokalizacjami.

require(['jquery',
				'js/modules/locations/sublocations-popover'],

function ($, ListView) {

"use strict";

var dropdown = null; // Aktywne menu
    
function clearDropdown () {
  if (!_.isNull(dropdown)) {
    dropdown.destroy();
  }
}

function enableDropdown (e) {
	$('.sublocation-menu-toggle').on('click', function (e) {
	  e.preventDefault();
	  e.stopPropagation();
	  clearDropdown();
	  dropdown = new ListView({
	    toggle: $(this),
	    id: $(this).attr('data-target')
	  });
	  $('body').not('.ancestors-menu').one('click', function (e) {
	    clearDropdown();
	  });
	});
}

$(document).ready(enableDropdown);

});
