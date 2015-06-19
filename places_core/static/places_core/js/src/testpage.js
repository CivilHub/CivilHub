//
// testpage.js
// ===========

// Te skrypty nie mają zastosowania na żadnej podstronie.
// Są tylko do testowania różnego stuffu.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'js/modules/inlines/list',
           'js/modules/common'],

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
    window.test = list;
    $(document).trigger('load');
  });
});
