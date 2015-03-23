// user-popup.js
// =============

// Żeby wywołać okienko z informacjami, wystarczy do dowolnego linku 
// związanego z użytkownikiem dodać parametr data-target równy 'pk' danego
// użytkownika oraz klasę 'user-window-toggle'.
	
require(['jquery', 'underscore', 'backbone'],

function ($, _, Backbone) {

"use strict";

// Timeout for popup window to open/close.
var timeout = null;

// Helper variable for delay functions.
var trigger = false;

// Another helper to check if some popup is already opened.
var state = false;

// User Backbone model

var UserModel = Backbone.Model.extend({});

// User Backbone view

var UserView  = Backbone.View.extend({
	tagName  : 'div',
	className: 'user-popup-window',
	template : _.template($('#user-popup-tpl').html()),
	events: {
		'click .user-popup-close': 'close'
	},
	render: function () {
		this.$el.html(this.template(this.model.toJSON()));
		return this;
	},
	close: function () {
		this.$el.empty().remove();
	}
});

// Backbone user collection

var UserCollection = Backbone.Collection.extend({
		model: UserModel
	});

// User popup window - replaces standard Backbone's collection view.

var UserPopupWindow = function (userdata, toggle) {
	this.model = new UserModel();
	this.collection = new UserCollection([userdata]);
	this.open = function () {
		state = true;
		this.collection.each(function (item) {
			var view  = new UserView({model:item}),
				$elem = $(view.render().el);
			$elem
				.appendTo('body')
				.offset({
					left: toggle.offset().left,
					top : toggle.offset().top - $elem.height()
				})
				.on('mouseout', function () {
					trigger = true;
					timeout = setTimeout(function () {
						if (trigger) {
							$elem.empty().remove();
						}
					}, 500);
				})
				.on('mouseover', function () {
					trigger = false;
					clearTimeout(timeout);
				});
		});
	};
	this.open();
};

// Bind events - open user popup window

var openWindow = function ($toggle) {
	var userId = $toggle.attr('data-target');
	$.get('/rest/users/' + userId, function (resp) {
		var win = new UserPopupWindow(resp, $toggle);
	});
};

$(document).ready(function () {
	$(document).delegate('.user-window-toggle', 'mouseover',
		function () {
			var $toggle = $(this);
			trigger = true;
			timeout = setTimeout(function () {
				if (trigger) {
					openWindow($toggle);
				}
			}, 500);
		}
	);

	$(document).delegate('.user-window-toggle', 'mouseout',
		function () {
			trigger = false;
			clearTimeout(timeout);
			if (state) {
				timeout = setTimeout(function () {
					$('.user-popup-window').empty().remove();
					state = false;
				}, 500);
			}
		}
	);
});

});