//
// idea-detail.js
// ==============
// 
// Szczegółowy widok pojedynczej idei.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/ideas/votes/counterWindow',
           'js/modules/common',
           'js/modules/ideas/votes/votes',
           'js/modules/comments/comments',
           'js/modules/maps/pointer',
           'js/modules/inviter/userinviter',
           'js/modules/locations/follow',
           'js/modules/ideas/category-creator'],

  function ($, CounterWindow) {
      
    "use strict";

    // Modal z podsumowanie głosów za i przeciw
    $('.idea-vote-count').on('click', function (e) {
      e.preventDefault();
      var ideaId = $(this).attr('data-target');
      var CW = CounterWindow.extend({
        'ideaId': ideaId
      });
      var cc = new CW();
    });
    
    $(document).trigger('load');
      
  });
});