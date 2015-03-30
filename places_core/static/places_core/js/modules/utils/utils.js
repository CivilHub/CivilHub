//
// utils.js
// ========

// Collection of different multi-purpose tools.

define(['jquery',
				'underscore',
				'bootbox'],

function ($, _) {
	
"use strict";

var utils = utils || {};

// Csrf protection methods.
// see: https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax

utils.csrfSafeMethod = function(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

utils.sameOrigin = function (url) {
	// test that a given url is a same-origin URL
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
};

// Get cookie by name
//
// @param {string} name Cookie's name
// @returns {string} Cookie's value

window.getCookie = utils.getCookie = function (name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
};

// Set cookie name and value
//
// @param { String } Cookie name
// @param { String } Cookie value
// @param { Number } Days to expire (optional)

utils.setCookie = function (name, value, days) {
	var date, expires;
  if (days) {
		date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		expires = "; expires="+date.toGMTString();
  }
  else expires = "";
  document.cookie = name+"="+value+expires+"; path=/";
};

// This function converts GET query into JSON. (Deprecated)
//
// @param { String } url address with parameters
// @returns { plain Object }

utils.urlToJSON = function (url) {
	var urlItems = [],
		jsonData = {},
		i, itm;
	url = url.split('?')[1] || false;
	if (!url) return {}; // Lack of GET data.
	url = url.split('&');
	for (i = 0; i < url.length; i++) {
		itm = url[i].split('=');
		jsonData[itm[0]] = itm[1];
	}
	return jsonData;
};

// This function serializes simple object into URL. (Deprecated)
//
// @param {JSON Obj} json object to conversion
// @returns { String } URL address parameters

utils.JSONtoUrl = function (json) {
	var pairs = _.pairs(json),
		urlitems = [],
		i;
	for (i = 0; i < pairs.length; i++) {
		urlitems.push(pairs[i].join('='));
	}
	return urlitems.join('&');
};

// This function gather additional data from the 'search' from. (Deprecated)

utils.getSearchText = function () {
	var $field = $('#haystack'),
		txt = $field.val();
	if (_.isUndefined(txt) || txt.length <= 1) {
		return false;
	}
	return txt;
};

// Loads selected options (Deprecated)
//
// Checks selected elements (clicked links)
// In order to "gather" browser options.

utils.getListOptions = function () {
	var $sel = $('.list-controller'),
		opts = {},
		optType = null,
		optValue = null,
		haystack = utils.getSearchText();
	$sel.each(function () {
		var $this = $(this);
		if ($this.hasClass('active')) {
			optType = $this.attr('data-control');
			optValue = $this.attr('data-target');
			opts[optType] = optValue;
		}
	});
	if (haystack !== false) {
		opts.haystack = utils.getSearchText();
	}
	return opts;
};

// The methods check whether the user is using a mobile device.
//
// @returns { Boolean }

utils.isMobile = function () {
	return (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent));
};

// This method check whether the user has Retina display.
//
// @returns { Boolean }

utils.isRetina = function () {
	return window.devicePixelRatio > 1;
};

return utils;

});