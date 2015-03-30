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

		$(document).ready(function () {
			$('#danger-button').on('click', function (e) {
				var $form = $(this).parents('form:first');
				e.preventDefault();
				ui.confirmWindow(function () {
					$form.submit();
				});
			});
		});

		$(document).trigger('load');

	});

});
