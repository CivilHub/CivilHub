//
// bookmarks.js
//
// Obsługa zakładek dla użytkownika

require(['jquery',
         'js/modules/ui/ui'],

function ($, ui) {

  "use strict";

  $(document).delegate('.btn-add-bookmark, .btn-remove-bookmark', 'click',

    function (e) {
      e.preventDefault();

      var $button = $(e.currentTarget),
        text = '',
        msg = '',
        data = {
          content_type: $button.attr('data-ct'),
          object_id: $button.attr('data-id')
        };

      $.post('/api-userspace/bookmarks/', data, function (created) {
        text = (created) ? "Remove bookmark" : "Bookmark";
        msg = (created) ? "Bookmark added" : "Bookmark removed";
        $button
          .toggleClass('btn-add-bookmark')
          .toggleClass('btn-remove-bookmark')
          .text(gettext(text));
        ui.message.success(msg);
      });
    }
  );

  // List of user's bookmarks to fetch.
  // -------------------------------------------------------------------------
  $(document).ready(function () {
    $('.bookmarks-list-toggle').one('click', function (evt) {
      $.get('/user/my_bookmarks', function (resp) {
        var $list = $('.bookmarks-list');
        resp = JSON.parse(resp);
        if (resp.success) {
          $(resp.bookmarks).each(function () {
            var $el = $('<li><a></a></li>'),
              href = this.target,
              label = this.label;
            $el.appendTo($list).find('a')
              .attr('href', href)
              .text(label);
          });
        }
      });
    });
  });
});