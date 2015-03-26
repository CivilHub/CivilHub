//
// tasks.js
// ========

// A script that handles the project summary.

require(['jquery',
         'js/modules/ui/ui'],

function ($, ui) {
  "use strict";

  function toggleTask (e) {
    var $this = $(e.currentTarget);
    var $form = $this.parent('form');
    $.post($form.attr('action'), null,
      function (response) {
        ui.message.success(response.message);
      }
    );
  }

  $(document).ready(function () {
    $('[name="checkbox-task"]').on('click', toggleTask);
  }); 
});