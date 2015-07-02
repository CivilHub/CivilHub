//
// votes.js
// ========

// App to manage idea votes.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'js/modules/ui/ui',
         'js/modules/ideas/votes/vote-area',
         'js/modules/ideas/votes/counterWindow'],

function ($, _, utils, ui, VoteArea, CounterWindow, html) {

"use strict";

// A window with vote summary.

var cw = null;

function send (id, data, fn, context) {
  data = data || {};
  data.csrfmiddlewaretoken = utils.getCookie('csrftoken');
  $.post('/ideas/vote/' + id + '/', data, function (response) {
    if (_.isFunction(fn)) {
      fn.call(context, response);
    }
  });
}

$(document).ready(function () {
  $('.idea-vote-count').on('click', function (e) {
    e.preventDefault();
    cw = new CounterWindow({
      ideaId: $(this).attr('data-target')
    });
  });
});

$.fn.voteArea = function () {
  return $(this).each(function () {
    var votes = new VoteArea({
      el: this
    });
    return this;
  });
};

$(document).ready(function () {
  $('.vote-form').voteArea();
});

});
