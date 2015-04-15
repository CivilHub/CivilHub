//
// counters.js
// ===========

// Scripts for visit counters. We are sending AJAX request
// to specific address when someone visits detail page with content.
// This scripts should be included only in such templates.

require(['jquery'],

function ($) {

"use strict";

function VisitCounter (el) {
  this.$el = $(el);
  this.ct = $(el).attr('data-ct');
  this.pk = $(el).attr('data-pk');
  $.get('/trigger-hit/' + this.ct + '/' + this.pk + '/',
    function (data) {
      return;
    }
  );
};

$.fn.visitCounter = function () {
  return $(this).each(function () {
    var counter = new VisitCounter(this);
    $(this).data('visit-counter', counter);
    return this;
  });
};

$(document).ready(function () {
  $('.visit-counter').visitCounter();
});

});
