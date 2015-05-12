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

utils.csrfSafeMethod = function (method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

utils.sameOrigin = function (url) {
  var host = document.location.host;
  var protocol = document.location.protocol;
  var srOrigin = '//' + host;
  var origin = protocol + srOrigin;
  return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
  (url == srOrigin || url.slice(0, srOrigin.length + 1) == srOrigin + '/') ||
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
  var date;
  var expires;
  if (days) {
    date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toGMTString();
  }
  else expires = "";
  document.cookie = name + "=" + value + expires + "; path=/";
};

// This function converts GET query into JSON. (Deprecated)
//
// @param { String } url address with parameters
// @returns { plain Object }

utils.urlToJSON = function (url) {
  var urlItems = [];
  var jsonData = {};
  var i;
  var itm;
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
  var pairs = _.pairs(json);
  var urlitems = [];
  var i;
  for (i = 0; i < pairs.length; i++) {
    urlitems.push(pairs[i].join('='));
  }
  return urlitems.join('&');
};

// This function gather additional data from the 'search' from. (Deprecated)

utils.getSearchText = function () {
  var $field = $('#haystack');
  var txt = $field.val();
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
  var $sel = $('.list-controller');
  var opts = {};
  var optType = null;
  var optValue = null;
  var haystack = utils.getSearchText();
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

utils.slugify = function (str) {
  return str.toLowerCase().replace(/[^\w ]+/g, '').replace(/ +/g, '-');
};

return utils;

});
