//
// discussion-form.js
// ==================
//
// A form for creation/edition of a discussion
//
//  => /templates/locations/location_forum_create.html
//
// -----------------------------------------------------------------------------

require(['jquery',
         'jqueryui',
         'redactor',
         'js/modules/ui/mapinput',
         'js/modules/content/content-form',
         'bootstrap-switch'],

function ($) {

  "use strict";

  $(document).ready(function () {

    $('#id_tags').tagsInput({
      autocomplete_url: '/rest/tags/',
      defaultText: gettext("Add tag")
    });

    $('#id_intro').redactor({
      buttons: ['bold', 'italic', 'unorderedlist', 'orderedlist', 'link', 'video'],
      plugins: ['uploader', 'video']
    });

    $('[type="checkbox"]').bootstrapSwitch({
      onText: gettext("Opened"),
      offText: gettext("Closed"),
      wrapperClass: 'form-group',
      onColor: 'success',
      offColor: 'danger'
    });
  });
});
