//
// votes.js
// ========

// App to manage idea votes.

require(['jquery',
         'underscore',
         'js/modules/utils/utils',
         'js/modules/ui/ui',
         'js/modules/ideas/votes/counterWindow'],

function ($, _, utils, ui, CounterWindow) {

  "use strict";

  // Okienko z podsumowaniem głosowania.

  var cw = null;

  $(document).ready(function () {
    $('.idea-vote-count').on('click', function (e) {
      e.preventDefault();
      cw = new CounterWindow({
        ideaId: $(this).attr('data-target')
      });
    });
  });

  // Głosowanie Tak lub Nie.

  $(document).delegate('.vote-btn-active', 'click', function () {

    var formData = {
        csrfmiddlewaretoken: utils.getCookie('csrftoken'),
        idea: $(this).attr('data-target-id'),
        vote: $(this).attr('data-vote')
      },

      $votes = $(this).parents('.idea-votes:first')
        .find('.votes:first'),

      $counter = $(this).parents('.idea-votes:first')
        .find('.idea-vote-count:first'),

      votes = parseInt($counter.text(), 10) || 0,

      callback = function (data) {
        if (data.success === true) {
          ui.message.success(data.message);
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