//
// summary.js
// ==========

// Comment summary page.

require(['jquery',
         'js/modules/inlines/list'],

function ($, CommentListView) {
  "use strict";
  var $el = $('#comment-area-test');
  var list = new CommentListView({
    $el: $el,
    url: '/api-comments/list/',
    ct: $el.attr('data-ct'),
    pk: $el.attr('data-pk'),
    count: $el.attr('data-count'),
    data: JSON.parse($el.attr('data-page')),
    currentPage: 1
  });
});
