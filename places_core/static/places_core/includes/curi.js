//
// magicUrl.js
// ===========

// Manage url params easily. This module allows you to perform GET and POST
// requests based on URL parameters. See README.md for details.
//
// This program is published on MIT license (see LICENSE.txt for details).
// You are allowed to use and modify it without further limitations.

define([], function () {

  "use strict";

  function getParams (url) {
    var re = new RegExp(/\?/);
    var params = {};
    var uri, tmp, i;
    if (re.test(url)) {
      uri = url.split('?')[1].split('&');
      url = url.split('?')[0];
      for (i = 0; i < uri.length; i++) {
        tmp = uri[i].split('=');
        params[tmp[0]] = tmp[1];
      }
    }
    return {url: url, params: params};
  }

  function urlFromParams (uriData) {
    var params = [];
    for (var prop in uriData.params) {
      if (uriData.params.hasOwnProperty(prop)) {
        params.push(([prop, uriData.params[prop]]).join('='));
      }
    }
    if (!params.length) {
      return uriData.url;
    }
    return ([uriData.url, params.join('&')]).join('?');
  }

  function CUri (url) {
    var tmpUrl = getParams(url);
    this.uri = tmpUrl.url;
    this.params = tmpUrl.params;
  }

  CUri.prototype.add = function (key, val) {
    this.params[key] = encodeURIComponent(val);
  };

  CUri.prototype.del = function (key) {
    delete this.params[key];
  };

  CUri.prototype.clear = function () {
    this.params = {};
  };

  CUri.prototype.url = function () {
    var url = this.uri;
    var par = this.params;
    return urlFromParams({url: url, params: par});
  };

  CUri.prototype.get = function (fn) {
    var req = new XMLHttpRequest();
    req.open('GET', this.url(), true);
    req.onreadystatechange = function () {
      if (req.readyState == 4) {
        if(req.status == 200 && fn !== undefined && typeof(fn) === 'function') {
          try {
            fn(JSON.parse(req.responseText));
          } catch (e) {
            fn(req.responseText);
          }
        }
      }
    };
    req.send(null);
  };

  CUri.prototype.post = function (fn) {
    var req = new XMLHttpRequest();
    req.open('POST', this.uri, true);
    req.onreadystatechange = function () {
      if (req.readyState == 4) {
        if(req.status == 200 && fn !== undefined && typeof(fn) === 'function') {
          try {
            fn(JSON.parse(req.responseText));
          } catch (e) {
            fn(req.responseText);
          }
        }
      }
    };
    req.send(this.params);
  };

  return CUri;
});