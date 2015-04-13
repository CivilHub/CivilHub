//
// poll-create.js
// ==============

// An interactive form for poll creation.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/common',
           'js/modules/locations/follow',
           'js/modules/inviter/userinviter',
           'js/modules/polls/poll-form/create-poll'],

  function ($) {
    "use strict";
    $(document).trigger('load');
  });
});
