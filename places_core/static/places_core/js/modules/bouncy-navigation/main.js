//
// main.js
// =======

// Skrypt uruchamiający bouncy-navigation w wersji dostosowanej
// dla Civil Hub. Pobieramy listę lokalizacji obserwowanych przez
// użytkownika i na tej podstawie tworzymy spersonalizowane menu.
// Skrypt uruchamiający samo menu jest bardzo prosty, większość
// siedzi w stylach.

require(['jquery',
				 'underscore',
				 'js/modules/bouncy-navigation/bouncy-navigation',
				 'js/modules/bouncy-navigation/bouncy-menu'],

function ($, _, BouncyNavigation) {
	"use strict";
	$(document).ready(function () {
		var nav = new BouncyNavigation(
			$('.cd-bouncy-nav-modal'),
			$('.cd-bouncy-nav-trigger')
		);
		nav.$modal.find('select').bouncyMenu();
	});
});