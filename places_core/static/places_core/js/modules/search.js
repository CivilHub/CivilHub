//
// search.js
// =========

// This script sends POST data to view recording searches performed by visitors.

require(['jquery',
         'underscore',
         'CUri',
         'js/modules/utils/utils'],

function ($, _, CUri, utils) {

"use strict";

$(document).ready(function () {
  var baseURL = '/report/search/';
  var activeURI = new CUri(document.location.href);
  if (_.isUndefined(activeURI.params.q)) {
    return;
  }
  activeURI.add('csrfmiddlewaretoken', utils.getCookie('csrftoken'));
  $.post(baseURL, activeURI.params, function (response) {
    console.log(response);
  });
});

});
