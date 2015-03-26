//
// main.js
// =======

// The script that launches the bouncy-navigation in a version
// adjusted to CivilHub. We download a list of followed locations
// by the user and on this basis we create a personalized menu.
// The script that  launches the menu itself if very simple,
// most of it is in styles.

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