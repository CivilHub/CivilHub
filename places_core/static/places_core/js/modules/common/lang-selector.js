//
// lang-selector.js
// ================

// Popover with language selection.

require(['jquery', 'bootstrap'], function ($) {

"use strict";

$(document).ready(function () {
	$('#lang-selector > a').popover({
		html: true,
		content: $('#popover-lang-list').html(),
		placement: 'top'
	});
	
	$('#lang-selector > a').on('shown.bs.popover', function () {
		$('.popover ul').find('a').on('click', function (e) {
			e.preventDefault();
			$('#lang-selected-field')
				.val($(this).parent().attr('data-code'));
			$('#main-lang-form').submit();
		});

		$('body').not('.popover ul').one('click', function () {
			$('#lang-selector > a').popover('hide');
			$('#popover-lang-list a').off('click');
		});
	});
});

});
