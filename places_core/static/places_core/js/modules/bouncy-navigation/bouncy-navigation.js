//
// bouncy-navigation.js
// ====================

// Dostosowana do projektu wersja pluginu. Patrz:
// http://codyhouse.co/gem/bouncy-navigation/

define(['jquery',
			  'underscore'],

function ($, _) {
"use strict";

// Funkcja pozwalająca nam uniezależnić animację przygotowaną
// przez autorów pluginu i wykorzystać na różnych elementach.
// Oczywiście, elementy muszą się zgadzać z budową pluginu.
//
// @param { jQuery.DomElement } Okno modala do otwarcia/zamknięcia
// @param { jQuery.DomElement } Przycisk uruchamiający animację menu
// @param { Boolean }	true otwiera menu, false zamyka
// @param { Function } Callback do wywołania po zakończeniu animacji

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

// Nawigacja musi zostać wywołana na $(document).ready.
// Inaczej nie zadziała.

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
		e.preventDefault();
		if($(e.target).is('.cd-bouncy-nav-modal')) {
			this._trigger(false);
		}
	}.bind(this));
};

return BouncyNavigation;

});
