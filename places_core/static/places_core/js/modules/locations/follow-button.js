//
// follow-button.js
// ================

// Follow button scripts ONLY FOR LOCATIONS!!!

define(['jquery',
        'js/modules/utils/utils',
        'js/modules/ui/ui'],

function ($, utils, ui) {

"use strict";

var fb = {

  url: '/api-locations/follow/?pk=',

  followRequest: function (pk, callback, context) {
    var token = utils.getCookie('csrftoken');
    $.post(this.url + pk, { csrfmiddlewaretoken: token },
      function (response) {
        ui.message.success(response.message);
        callback.call(context, response);
      }
    );
  },

  settext: function (following) {
    return following ? gettext("Stop following")
                     : gettext("Follow");
  }
};

return fb;

});
