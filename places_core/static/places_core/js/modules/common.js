//
// common.js
// =========

// Simple common scripts, such as tooltips etc.

define(['jquery',
				'bootstrap',
				'jpaginate',
				'js/modules/locations/sublocations',
				'js/modules/common/toggle-menu',
				'js/modules/common/lang-selector',
				'js/modules/common/bookmarks',
				'js/modules/common/tour',
				'js/modules/common/tag-cloud',
				'js/modules/common/abuse-report',
				'js/modules/common/cookie-warning',
				'js/modules/common/messages',
				'js/modules/ui/widgets',
				'js/modules/userspace/user-popup',
				'js/modules/bouncy-navigation/main'],

function ($) {
	
"use strict";

// "Static" pagination
// ---------------------

$('.custom-static-pagination').pagination({
	visibleEntries: 13
});

//textarea increases the height
$('textarea').keypress(function (e) {
  // check if user pressed 'Enter'
  if(e.which == 13) {
	// get control object to modify further
	var control = e.target;
	// get existing 'Height' of pressed control
	var controlHeight = $(control).height();
	// add some height to existing height of control, I chose 17
	// as my line-height was 17 for the control.
	$(control).height(controlHeight + 17);
  }
});

// Common simple scripts.
// -------------------------------------------------------------------------

// Cancel button for some forms which allow back one page.
$('.cancel-btn').on('click', function () {
	history.go(-1);
});
// Tooltips for elements shared among templates.
$('.navbar-avatar').tooltip({placement: 'bottom'});
$('.custom-tooltip').tooltip();
$('.custom-tooltip-bottom').tooltip({
	placement: 'bottom'
});
$('.custom-tooltip-right').tooltip({
	placement: 'right'
});

// Scroll to top button
// -------------------------------------------------------------------------

$(document).ready(function () {
	
	var $scrollButton = $(document.createElement('a'));
	
	$scrollButton.attr({
		'id': 'scrollToTop',
		'href': '#top',
		'name': gettext('Scroll to top')
	});
	
	$('.wrap').append($scrollButton);
	
	if($(window).scrollTop()<300)
		$scrollButton.hide();
		
	$scrollButton.click(function() {
		$("html, body").animate({ scrollTop: 0 }, "slow");
		return false;
	});

	$(window).scroll(function(){
		if($(window).scrollTop()>300) {
			$scrollButton.fadeIn('slow');
		} else {
			$scrollButton.fadeOut('slow');
		}
	});
});

});