//
// tasks.js
// ========

// A script that handles the project summary.

require(['jquery',
         'js/modules/ui/ui',
         'js/modules/utils/utils'],

function ($, ui, utils) {

"use strict";

function toggleTask (e) {
  var $this = $(e.currentTarget);
  var $form = $this.parent('form');
  var data = { csrfmiddlewaretoken: utils.getCookie('csrftoken') };
  $.post($form.attr('action'), data,
    function (response) {
      ui.message.success(response.message);
    }
  );
}

$(document).ready(function () {
  $('[name="checkbox-task"]').on('click', toggleTask);
});

});
