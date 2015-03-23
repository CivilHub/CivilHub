//
// toggle-menu.js
// ==============

// Otwiera menu z opcjami w widokach szczegółowych
// różnych typów zawartości po kliknięciu w przycisk.

require(['jquery'], function ($) {

"use strict";

function SubMenu ($el) {
	this.$el = $el;
	this.is_menu_opened = false;
	this.$submenu = this.$el
		.parent()
		.next('.entry-submenu');
	this.initialize();
}

SubMenu.prototype.initialize = function () {
  this.$el.on('click', function (e) {
  	e.preventDefault();
  	SubMenu.prototype.toggle.call(this);
  }.bind(this));
};

SubMenu.prototype.open = function () {
	this.$submenu.slideDown('fast', function () {
		$('body').one('click', function () {
			this.close();
		}.bind(this));
		this.is_menu_opened = true;
	}.bind(this));
};

SubMenu.prototype.close = function () {
	this.$submenu.slideUp('fast', function () {
		this.is_menu_opened = false;
	}.bind(this));
};

SubMenu.prototype.toggle = function () {
	if (this.is_menu_opened)
		this.close();
	else
		this.open();
};

$.fn.simpleSubMenu = function () {
	return $(this).each(function () {
		$(this).data('submenu', new SubMenu($(this)));
	});
};

$(document).ready(function () {
	$('.submenu-toggle').simpleSubMenu();
});

});
