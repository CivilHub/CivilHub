//
// location-create.js
// ==================

// New location creation

require([window.STATIC_URL + "/js/config.js"], function () {
	require(['jquery',
					 'js/modules/locations/location-form',
					 'js/modules/ui/ui',
					 'js/modules/common'],

	function ($, LocationForm, ui) {

		"use strict";

		$(document).ready(function () {
			var form = new LocationForm();
		});

		$(document).trigger('load');

	});

});
