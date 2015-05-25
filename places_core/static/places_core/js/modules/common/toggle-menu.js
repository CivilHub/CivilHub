//
// toggle-menu.js
// ==============

// Opens a menu with options in detailed views
// of various types of content after clicking a button

require(['jquery'], function ($) {

"use strict";

function SubMenu ($el) {
  this.$el = $el;
  this.isMenuOpened = false;
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
    this.isMenuOpened = true;
  }.bind(this));
};

SubMenu.prototype.close = function () {
  this.$submenu.slideUp('fast', function () {
    this.isMenuOpened = false;
  }.bind(this));
};

SubMenu.prototype.toggle = function () {
  if (this.isMenuOpened)
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
