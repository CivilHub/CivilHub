//
// hotbox.js
// =========

// Show list of last news entries.

require(['jquery',
         'js/modules/hotbox/view'],

function ($, HotBox) {

"use strict";

var baseUrl = '/api-hitcounter/hot-box/';

$.fn.hotBoxInitializer = function () {
  return $(this).each(function () {
    var $this = $(this);
    var url = ([
      baseUrl, '?', $this.attr('data-param'),
      '=', $this.attr('data-value')
    ]).join('');
    var hotbox = new HotBox({
      appendTo: $this,
      url: url
    });
    $this.data('hotbox', hotbox);
    return this;
  });
};

$(document).ready(function () {
  $('.hotbox').hotBoxInitializer();
});

});
