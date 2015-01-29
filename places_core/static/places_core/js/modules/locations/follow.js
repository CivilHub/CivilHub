//
// follow.js
// =========
//
// Obsługa przycisków 'follow location' i 'stop following'.

require(['jquery',
         'js/modules/ui/ui'],

function ($, ui) {
    
  "use strict";

  var sendFollowRequest = function (e) {
      
    var $button = $(e.currentTarget),
    
      follow = $button.hasClass('btn-follow-location'),
  
      url = (follow) ? '/locations/add_follower/{id}/'
                     : '/locations/remove_follower/{id}/',
                     
      txt = (follow) ? gettext('You are following') : gettext('Follow');
        
    url = url.replace(/{id}/g, $button.attr('data-location-id'));

    $.post(url, {csrfmiddlewaretoken: getCookie('csrftoken')},
      function (resp) {
        resp = JSON.parse(resp);
        if (resp.success) {
          ui.message.success(resp.message);
          $button
            .toggleClass('btn-follow-location')
            .toggleClass('btn-unfollow-location')
            .text(txt);
        } else {
          ui.message.alert(resp.message);
        }
      }
    );
  };
  
  $(document).ready(function () {
    $('.btn-follow-location, .btn-unfollow-location')
      .on('click', sendFollowRequest);
  });
});