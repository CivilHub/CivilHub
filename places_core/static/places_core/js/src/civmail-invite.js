//
// civmail-invite.js
// =================

// A scirpt for "Zaproś znajomych" [eng. invite a friend] site

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'tagsinput',
           'js/modules/common',
           'js/modules/userspace/enable-contacts'],

  function ($) {

    "use strict";

    $(document).ready(function () {
      var $emails = $('[name="emails"]');
      $emails.tagsInput({
        defaultText: '',
        onPaste: true,
        onAddTag: function () {
          var oldValue = $emails.val();
          var newValue = oldValue.replace(/ /g, ',');
          $emails.importTags('');
          $emails.importTags(newValue);
        }
      });
    });

    $(document).trigger('load');

  });
});
