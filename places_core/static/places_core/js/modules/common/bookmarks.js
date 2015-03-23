//
// bookmarks.js
// ============

// Obsługa zakładek dla użytkownika

require(['jquery',
         'js/modules/utils/utils',
         'js/modules/ui/ui'],

function ($, utils, ui) {

"use strict";

var entryTemplate = '<li><a href="{link}">{label}</a></li>';

function makeRequest (url, data, callback) {
  $.post(url, data, function (response) {
    if (response.success) {
      ui.message.success(response.message);
      if (callback !== undefined && typeof(callback === 'function')) {
        callback(response);
      }
    } else {
      ui.message.alert(response.message);
    }
  });
}

// Add/remove bookmark via AJAX API
// --------------------------------

$(document).delegate('.btn-bookmark', 'click', function (e) {

  e.preventDefault();

  var $this = $(e.currentTarget);

  var postData = null, url = '';

  if ($this.hasClass('btn-add-bookmark')) {
    // Dodajemy nową zakładkę
    postData = {
      object_id: $this.attr('data-id'),
      content_type: $this.attr('data-ct'),
      csrfmiddlewaretoken: getCookie('csrftoken')
    };
    
    makeRequest('/bookmarks/create/', postData, function (resp) {
      $this
        .removeClass('btn-add-bookmark')
        .addClass('btn-active-bookmark')
        .attr('data-pk', resp.bookmark)
        .text(gettext("Remove bookmark"));
    });

  } else {

    // Usuwamy zakładkę

    url = '/bookmarks/delete/{}/'.replace(/{}/g, $this.attr('data-pk'));
    postData = {csrfmiddlewaretoken: utils.getCookie('csrftoken')};
    
    makeRequest(url, postData, function (resp) {
      $this
        .removeClass('btn-active-bookmark')
        .addClass('btn-add-bookmark')
        .text(gettext("Add bookmark"));
    });
  }
});

// List of user's bookmarks to fetch
// ---------------------------------

$(document).ready(function () {
  $('.bookmarks-list-toggle').one('click', function (evt) {
    $.get('/api-userspace/my-bookmarks/', function (resp) {
      var $list = $('.bookmarks-no-list');
      $(resp).each(function () {
        var html = entryTemplate.replace(/{link}/g, this.url)
          .replace(/{label}/g, this.label);
        $(html).insertBefore($list.find('.divider:last'));
      });
    });
  });
});

});
