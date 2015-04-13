//
// postman-write.js
// ================

// Scripts that handle Postman mailbox

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'underscore',
           'js/modules/common'],

  function ($, _) {

    "use strict";

    function fakeUserInput () {
      var tpl = _.template($('#fake-recipient-tpl').html());
      var url = '/rest/users/?username=' + $('#id_recipients').val();
      $.get(url, function (data) {
        $('#fake_recipients').html(tpl(data));
      });
    }

    $(document).ready(fakeUserInput);

    $(document).trigger('load');

  });
});
