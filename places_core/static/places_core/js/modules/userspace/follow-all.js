//
// follow-all.js
// =============

// Follow all FB friends with one click.

require(['jquery',
         'underscore',
         'js/modules/ui/ui',
         'js/modules/utils/utils'],

function ($, _, ui, utils) {

"use strict";

var url = "/api-activities/follow-all/";

function sendPost(data, fn, context) {
  data.csrfmiddlewaretoken = utils.getCookie('csrftoken');
  $.post(url, data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

function followAll() {
  var ids = _.map($('.civ-follow-btn'), function (item) {
    return $(item).attr('data-pk');
  });
  sendPost({ id: ids.join(',') }, function (response) {
    ui.message.success(response.message);
    $('.civ-follow-btn')
      .removeClass('btn-follow')
      .addClass('btn-unfollow')
      .text(response.label);
  });
}

$(document).ready(function () {
  $('#follow-all').on('click', function (e) {
    e.preventDefault();
    followAll();
  });
});

});
