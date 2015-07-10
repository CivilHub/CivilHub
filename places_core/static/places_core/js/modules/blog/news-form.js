//
// news-form.js
// ============

require(['jquery',
         'jqueryui',
         'js/modules/editor/plugins/uploader',
         'redactor',
         'tagsinput',
         'js/modules/content/content-form'],

function ($) {

  "use strict";

  $(document).ready(function () {

    var map = null;

    $('#id_content').redactor({
      buttons: ['bold', 'italic', 'unorderedlist', 'orderedlist', 'link', 'video'],
      plugins: ['uploader', 'video']
    });

    $('#id_tags').tagsInput({
      autocomplete_url: '/rest/tags/',
      defaultText: gettext("Add tag")
    });
  });

});
