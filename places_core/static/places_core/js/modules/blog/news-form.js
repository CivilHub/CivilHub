//
// news-form.js
// ============

require(['jquery',
         'redactor',
         'tagsinput',
         'js/modules/content/content-form'],

function ($) {

  "use strict";

  $(document).ready(function () {

    var map = null;

    $('#id_content').redactor({
      buttons: ['bold', 'italic', 'unorderedlist', 'orderedlist', 'link'],
      plugins: ['uploader']
    });

    $('#id_tags').tagsInput({
      autocomplete_url: '/rest/tags/',
      defaultText: gettext("Add tag")
    });
  });

});
