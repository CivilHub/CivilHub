//
// votes.js
// ========

// App to manage idea votes.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'js/modules/ui/ui',
         'js/modules/ideas/votes/counterWindow',
         'text!js/modules/ideas/templates/share-modal.html'],

function ($, _, utils, ui, CounterWindow, html) {

"use strict";

// A window with vote summary.

var cw = null;

$(document).ready(function () {
  $('.idea-vote-count').on('click', function (e) {
    e.preventDefault();
    cw = new CounterWindow({
      ideaId: $(this).attr('data-target')
    });
  });
});

// Share content after voting

function openShareWindow () {
  var tpl = _.template(html);
  var $el = $(tpl({
    token: CivilApp.fbClientToken,
    url: document.location.href,
    title: document.title
  }));
  $el.modal();
  $el.find('.trigger-link').on('click', function (e) {
    e.preventDefault();
    window.open($(this).attr('href'), $(this).text(),
      "width=600,height=350,menubar=0,status=0,resizable=1");
  });
  $el.find('a').on('click', function (e) {
    e.preventDefault();
    $el.modal('hide');
  });
}

// Vote Yes or No.

$(document).delegate('.vote-btn-active', 'click', function () {

  var formData = {
    csrfmiddlewaretoken: utils.getCookie('csrftoken'),
    idea: $(this).attr('data-target-id'),
    vote: $(this).attr('data-vote')
  };

  var $votes = $(this).parents('.idea-votes:first')
        .find('.votes:first');

  var $counter = $(this).parents('.idea-votes:first')
        .find('.idea-vote-count:first');

  var votes = parseInt($counter.text(), 10) || 0;

  function callback (data) {
    if (data.success === true) {
      ui.message.success(data.message);
      openShareWindow();
      $votes.html(data.votes);
      if (!_.isNaN(votes)) {
        $counter.text(++votes);
      } else {
        $counter.text(0);
      }
    } else {
      ui.message.warning(data.message);
    }
  };

  $.post('/ideas/vote/', formData, callback);
});

});
