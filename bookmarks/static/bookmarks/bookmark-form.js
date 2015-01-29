/*
 * bookmark-form.js
 * 
 * Obsługa dodawania i usuwania zakładek użytkownika via AJAX.
 * Skrypt współpracuje z tagiem `bookmark_form` z grupy `bookmark_tags`.
 * Do działania wymaga jQuery oraz flash-msg z mojego repozytorium.
 */
(function ($, msg) {
  
  "use strict";
  
  msg.initialize();
  
  function getCookie (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
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
  }
  
  function makeRequest (url, data, callback) {
    $.post(url, data, function (response) {
      if (response.success) {
        msg.success(response.message);
        if (callback !== undefined && typeof(callback === 'function')) {
          callback(response);
        }
      } else {
        msg.alert(response.message);
      }
    });
  }
  
  $(document).delegate('.btn-bookmark', 'click', function (e) {
    e.preventDefault();
    var $this = $(e.currentTarget);

    if ($this.hasClass('btn-add-bookmark')) {
      // Dodajemy nową zakładkę
      var postData = {
        object_id: $this.attr('data-id'),
        content_type: $this.attr('data-ct'),
        csrfmiddlewaretoken: getCookie('csrftoken')
      };
      
      makeRequest('/bookmarks/create/', postData, function (resp) {
        $this
          .removeClass('btn-add-bookmark')
          .addClass('btn-active-bookmark')
          .attr('data-pk', resp.bookmark)
          .attr("data-original-title", "Usuń zakładkę");
      });

    } else {
      // Usuwamy zakładkę
      var postData = {csrfmiddlewaretoken: getCookie('csrftoken')};
      var url = '/bookmarks/delete/{}/'.replace(/{}/g, $this.attr('data-pk'));
      
      makeRequest(url, postData, function (resp) {
        $this
          .removeClass('btn-active-bookmark')
          .addClass('btn-add-bookmark')
          .attr("data-original-title", "Dodaj do zakładek");
      });
    }
  });
  
})(jQuery, msg);