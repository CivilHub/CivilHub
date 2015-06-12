//
// http.js
// =======

// Misc utils to use along entire application targeting to
// process and simplify different HTTP operations.

define(['jquery',
        'underscore'],

function ($, _) {

"use strict";

var http = {};

// Handy wrapper for HTTP GET requests. Allows us to pass additional 'context'
// variable that will became 'this' value in callback function.

// @param { String } Url address to fetch from
// @param { Plain Object } Additional parameters to pass as GET
// @param { Function } Callback function to trigger on success (optional)
// @param { Object } Any object that you want to get as 'this'.

http.fetch = function (url, data, fn, context) {
  $.get(url, data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
};

return http;

});
