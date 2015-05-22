//
// comments.js
// ===========

// Initializes the comment application.

require(['jquery',
         'js/modules/inlines/list'],

function ($, CommentListView) {

"use strict";

var BASEURL = '/api-comments/';

$.fn.commentList = function () {
  return $(this).each(function () {
    var $this = $(this);
    var commentlist = new CommentListView({
      $el: $this,
      url: BASEURL + 'list/',
      ct: $this.attr('data-ct'),
      pk: $this.attr('data-pk'),
      count: $this.attr('data-count'),
      currentPage: 1
    });
    $this.data('commentlist', commentlist);
    commentlist.fetch();
    $(window).on('scroll', function () {
      if ($(window).scrollTop() >= $(document).height() - $(window).height()) {
        commentlist.nextPage();
      }
    });
  });
};

$(document).ready(function () {
  $('.commentarea').commentList();
});

});
