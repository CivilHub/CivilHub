//
// document-form.js
// ================

// Provides pad creation form in handy modal window.
// Performs json request and server-side validation.

require(['jquery'],

function ($) {

"use strict";

// Simple alert template for error message

var ERR_TPL = '<div class="alert alert-danger">{}</div>';

// Little helper converting data from serializeArray to object notation.

function processData (data) {
	var processed = {};
	$.each(data, function (idx, itm) {
		processed[itm.name] = itm.value;
	});
	return processed;
}

function submitForm (e) {
	var $f = $('#' + $(e.currentTarget)
		.attr('data-submits'));
	var $modal = $(e.currentTarget).parents('.modal');
	var $input = $modal.find('[type="text"]');
	$('#id_name').val($input.val());
	var data = processData($f.serializeArray());

	// Clear all old messages
	$modal.find('.alert').empty().remove();

	// We just reloads page if no errors are present
	$.post($f.attr('action'), data, function (response) {
		if (response.errors === undefined) {
			document.location.href = document.location.href;
			return false;
		}
		$input.before($(ERR_TPL
			.replace(/{}/g, response.errors.name[0])));
	});
}

function runScripts () {
	var $form = $('#pad-creation-form');
	var $modal = $('#pad-creation-modal');

	// Submit real form when user enter new title
	$modal.modal({show: false});

	// Remove all previous alert messages
	$modal.find('.alert').empty().remove();
	$modal.find('[data-submits]')
		.on('click', submitForm);

	// Hide original form inputs
	$form.find('label, input').hide();
	$form.find('[type="submit"]').on('click',
		function (e) {
			e.preventDefault();
			$modal.modal('toggle');
		}
	);
}

$(document).ready(runScripts);

});
