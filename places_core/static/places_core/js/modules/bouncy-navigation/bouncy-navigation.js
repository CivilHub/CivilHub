//
// bouncy-navigation.js
// ====================

// An adjusted to the project version of the plugin. See:
// http://codyhouse.co/gem/bouncy-navigation/

define(['jquery',
			  'underscore'],

function ($, _) {
"use strict";

// This function allows us to make independent the animation prepared
// by the authors of the plugin and make use of it on certain
// elements. Of course, the elements must fit the plugin's structure.
//
// @param { jQuery.DomElement } Modal Windows to open/close
// @param { jQuery.DomElement } A button that launches the animation
// @param { Boolean }	true opens the menu, false closes it
// @param { Function } Callback to call after the animation is completed

function triggerAnimation ($modal, $trigg, open, fn) {
	//toggle list items animation
	open = (!_.isUndefined(open)) ? open : true;
	$modal
		.toggleClass('fade-in', open)
		.toggleClass('fade-out', !open)
		.find('li:last-child').one('webkitAnimationEnd oanimationend msAnimationEnd animationend',
			function () {
				$modal.toggleClass('is-visible', open);
				if(!open) $modal.removeClass('fade-out');
				if (_.isFunction(fn)) fn();
			}
		);
	
	//check if CSS animations are supported... 
	if($trigg.parents('.no-csstransitions').length > 0 ) {
		$modal.toggleClass('is-visible', open);
		if (_.isFunction(fn)) fn();
	}
}

// The navigation must be called on $(document).ready.
// Else it will not work 

function BouncyNavigation ($modal, $trigger) {
	this.is_bouncy_nav_animating = false;
	this.$modal = $modal;
	this.$trigger = $trigger;
	this.initialize();
}

BouncyNavigation.prototype._trigger = function (open) {
	var flag = this.is_bouncy_nav_animating;
	if (!this.is_bouncy_nav_animating) {
		triggerAnimation(this.$modal, this.$trigger, open,
			function () {
				flag = false;
			}
		);
	}
};

BouncyNavigation.prototype.initialize = function () {
	this.$trigger.on('click', function (e) {
		e.preventDefault();
		this._trigger(true);
	}.bind(this));
	this.$modal.find('.cd-close').on('click', function (e) {
		e.preventDefault();
		this._trigger(false);
	}.bind(this));
	this.$modal.on('click', function (e) {
		if($(e.target).is('.cd-bouncy-nav-modal')) {
			this._trigger(false);
		}
	}.bind(this));
};

return BouncyNavigation;

});
